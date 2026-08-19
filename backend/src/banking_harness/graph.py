"""Authoritative Product/Process Change graph with bounded agents and HITL."""

from __future__ import annotations

import operator
from typing import Annotated, Any, Literal
from uuid import uuid4

from langgraph.graph import END, START, StateGraph
from langgraph.types import Command, Send, interrupt
from typing_extensions import TypedDict

from .evals import evaluate_case, release_gate
from .knowledge import KnowledgeProvider, SourceDocument, configured_knowledge_provider
from .model_gateway import ModelGateway
from .models import CaseStatus, ChangeRequest, EvidenceEvent, HumanDecision, RequestClass


class CaseState(TypedDict, total=False):
    case_id: str
    status: str
    request: dict[str, Any]
    classification: str
    missing_evidence: list[str]
    sources: list[dict[str, Any]]
    impact_domain: str
    findings: Annotated[list[dict[str, Any]], operator.add]
    eval_results: list[dict[str, Any]]
    eval_iteration: int
    model_usage: Annotated[list[dict[str, Any]], operator.add]
    evidence_events: Annotated[list[dict[str, Any]], operator.add]
    human_decision: dict[str, Any]
    controlled_action: dict[str, Any]


def _event(event: str, actor: str, detail: str) -> list[dict[str, Any]]:
    return [EvidenceEvent(event=event, actor=actor, detail=detail).model_dump()]


def _request(state: CaseState) -> ChangeRequest:
    return ChangeRequest.model_validate(state["request"])


def build_product_change_graph(
    *,
    knowledge: KnowledgeProvider | None = None,
    model_gateway: ModelGateway | None = None,
    checkpointer: Any | None = None,
):
    """Compile the product-change process package into a durable LangGraph."""

    knowledge = knowledge or configured_knowledge_provider()
    model_gateway = model_gateway or ModelGateway()

    def register(state: CaseState) -> dict[str, Any]:
        request = _request(state)
        return {"status": CaseStatus.RUNNING.value, "eval_iteration": 1, "evidence_events": _event("case_registered", request.owner, "Original request preserved before model processing.")}

    def classify(state: CaseState) -> dict[str, Any]:
        request = _request(state)
        classification = RequestClass.CHANGE_TO_EXISTING.value if request.existing_item_id else RequestClass.NEW_IMPLEMENTATION.value
        return {"classification": classification, "evidence_events": _event("request_classified", "classification_agent", f"{classification}/{request.subject_type.value}")}

    def validate_evidence(state: CaseState) -> dict[str, Any]:
        request = _request(state)
        required = {"risk_reference": request.risk_reference, "legal_reference": request.legal_reference, "infosec_reference": request.infosec_reference, "related_department_reference": request.related_department_reference}
        if request.aml_applicable:
            required["aml_reference"] = request.aml_reference
        missing = [name for name, value in required.items() if not value]
        return {"missing_evidence": missing, "evidence_events": _event("evidence_validated", "policy_engine", "Complete" if not missing else f"Missing {', '.join(missing)}")}

    def route_validation(state: CaseState) -> Literal["retrieve_source", "request_information"]:
        return "request_information" if state.get("missing_evidence") else "retrieve_source"

    def request_information(state: CaseState) -> dict[str, Any]:
        return {"status": CaseStatus.NEEDS_INFORMATION.value, "evidence_events": _event("information_requested", "workflow_engine", f"Case paused: {', '.join(state['missing_evidence'])}")}

    def retrieve_source(state: CaseState) -> dict[str, Any]:
        request = _request(state)
        sources = knowledge.search(f"{request.title} {request.requested_change}")
        return {"sources": [item.__dict__ for item in sources], "evidence_events": _event("sources_retrieved", "bank_memory", ", ".join(f"{item.source_id}@{item.version}" for item in sources))}

    def dispatch_impacts(state: CaseState) -> list[Send]:
        payload = {"case_id": state["case_id"], "request": state["request"], "sources": state["sources"]}
        return [Send("impact_worker", {**payload, "impact_domain": domain}) for domain in ("risk", "operations", "technology")]

    def impact_worker(state: CaseState) -> dict[str, Any]:
        sources = [SourceDocument(**item) for item in state["sources"]]
        finding, usage = model_gateway.analyze_impact(state["impact_domain"], _request(state), sources)
        return {"findings": [finding.model_dump()], "model_usage": [usage.__dict__], "evidence_events": _event("impact_prepared", f"{state['impact_domain']}_impact_agent", f"{finding.severity} severity finding with {len(finding.citations)} citation(s).")}

    def evaluate(state: CaseState) -> dict[str, Any]:
        from .models import ImpactFinding

        findings = [ImpactFinding.model_validate(item) for item in state.get("findings", [])]
        results = evaluate_case(_request(state), findings, state.get("missing_evidence", []))
        return {"eval_results": [result.model_dump() for result in results], "evidence_events": _event("case_evaluated", "eval_service", f"{sum(result.passed for result in results)}/{len(results)} gates passed.")}

    def route_eval(state: CaseState) -> Literal["human_review", "eval_escalation"]:
        from .models import EvalResult

        results = [EvalResult.model_validate(item) for item in state["eval_results"]]
        return "human_review" if release_gate(results) else "eval_escalation"

    def eval_escalation(state: CaseState) -> dict[str, Any]:
        return {"status": CaseStatus.EVAL_ESCALATION.value, "evidence_events": _event("eval_escalated", "eval_service", "Automated release gate failed; human resolution required.")}

    def human_review(state: CaseState) -> Command[Literal["prepare_controlled_action", "finish"]]:
        # interrupt is intentionally the first operation: code before it reruns on resume.
        response = interrupt({"kind": "product_support_approval", "case_id": state["case_id"], "title": _request(state).title, "findings": state["findings"], "eval_results": state["eval_results"], "allowed_decisions": ["approve", "reject"]})
        decision = HumanDecision.model_validate(response)
        update = {"human_decision": decision.model_dump(), "evidence_events": _event(f"human_{decision.decision}", decision.reviewer, decision.comment or decision.decision)}
        if decision.decision == "approve":
            update["status"] = CaseStatus.APPROVED.value
            return Command(update=update, goto="prepare_controlled_action")
        update["status"] = CaseStatus.REJECTED.value
        return Command(update=update, goto="finish")

    def prepare_controlled_action(state: CaseState) -> dict[str, Any]:
        # This is a proposal only; no authoritative bank system is mutated.
        return {"controlled_action": {"type": "CREATE_DEPARTMENT_REVIEW_TASKS", "mode": "SIMULATED", "case_id": state["case_id"]}, "evidence_events": _event("controlled_action_prepared", "workflow_engine", "Synthetic review tasks prepared; no external write executed.")}

    def finish(_: CaseState) -> dict[str, Any]:
        return {}

    builder = StateGraph(CaseState)
    builder.add_node("register", register).add_node("classify", classify).add_node("validate_evidence", validate_evidence)
    builder.add_node("request_information", request_information).add_node("retrieve_source", retrieve_source)
    builder.add_node("impact_worker", impact_worker).add_node("evaluate", evaluate).add_node("eval_escalation", eval_escalation)
    builder.add_node("human_review", human_review).add_node("prepare_controlled_action", prepare_controlled_action).add_node("finish", finish)
    builder.add_edge(START, "register").add_edge("register", "classify").add_edge("classify", "validate_evidence")
    builder.add_conditional_edges("validate_evidence", route_validation, ["request_information", "retrieve_source"])
    builder.add_edge("request_information", END).add_conditional_edges("retrieve_source", dispatch_impacts, ["impact_worker"])
    builder.add_edge("impact_worker", "evaluate").add_conditional_edges("evaluate", route_eval, ["human_review", "eval_escalation"])
    builder.add_edge("eval_escalation", END).add_edge("prepare_controlled_action", "finish").add_edge("finish", END)
    return builder.compile(checkpointer=checkpointer)


def new_case_input(request: ChangeRequest, case_id: str | None = None) -> CaseState:
    return {"case_id": case_id or f"CASE-{uuid4().hex[:8].upper()}", "request": request.model_dump(), "findings": [], "model_usage": [], "evidence_events": []}
