"""FastAPI boundary for starting and resuming governed cases."""

from __future__ import annotations

import os
import secrets
from contextlib import asynccontextmanager
from typing import Any

from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from langgraph.types import Command

from .checkpointing import CheckpointRuntime
from .graph import build_product_change_graph, new_case_input
from .models import ChangeRequest, HumanDecision

runtime = CheckpointRuntime()
graph = build_product_change_graph(checkpointer=runtime.get())
known_cases: set[str] = set()
api_token = os.getenv("HARNESS_API_TOKEN", "")


def require_api_token(authorization: str | None = Header(default=None)) -> None:
    if not api_token:
        raise HTTPException(
            status_code=503,
            detail="Set HARNESS_API_TOKEN before using case endpoints.",
        )
    scheme, _, supplied = (authorization or "").partition(" ")
    if scheme.lower() != "bearer" or not secrets.compare_digest(supplied, api_token):
        raise HTTPException(status_code=401, detail="Invalid API token.")


@asynccontextmanager
async def lifespan(_: FastAPI):
    try:
        yield
    finally:
        runtime.close()


app = FastAPI(title="Banking AI Core Harness API", version="0.1.0", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"], allow_methods=["GET", "POST"], allow_headers=["Content-Type", "Authorization"])


def _interrupts(result: dict[str, Any]) -> list[dict[str, Any]]:
    return [{"id": item.id, "value": item.value} for item in result.get("__interrupt__", [])]


@app.get("/health")
def health() -> dict[str, Any]:
    return {"status": "ok", "runtime": "langgraph", "durable_checkpoints": bool(runtime.database_url)}


@app.post("/cases", dependencies=[Depends(require_api_token)])
def create_case(request: ChangeRequest) -> dict[str, Any]:
    state = new_case_input(request)
    case_id = state["case_id"]
    known_cases.add(case_id)
    result = graph.invoke(state, {"configurable": {"thread_id": case_id}})
    return {"case_id": case_id, "state": result, "interrupts": _interrupts(result)}


@app.get("/cases/{case_id}", dependencies=[Depends(require_api_token)])
def get_case(case_id: str) -> dict[str, Any]:
    if case_id not in known_cases:
        raise HTTPException(status_code=404, detail="Unknown case.")
    snapshot = graph.get_state({"configurable": {"thread_id": case_id}})
    return {"case_id": case_id, "state": snapshot.values, "next": snapshot.next}


@app.post("/cases/{case_id}/decision", dependencies=[Depends(require_api_token)])
def decide_case(case_id: str, decision: HumanDecision) -> dict[str, Any]:
    if case_id not in known_cases:
        raise HTTPException(status_code=404, detail="Unknown case.")
    result = graph.invoke(Command(resume=decision.model_dump()), {"configurable": {"thread_id": case_id}})
    return {"case_id": case_id, "state": result, "interrupts": _interrupts(result)}
