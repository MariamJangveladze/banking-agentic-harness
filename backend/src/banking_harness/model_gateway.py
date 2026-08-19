"""Policy-aware model seam with deterministic and optional local Ollama routes."""

from __future__ import annotations

import os
from dataclasses import dataclass

from .knowledge import SourceDocument
from .models import ChangeRequest, Citation, ImpactFinding


@dataclass(frozen=True)
class ModelUsage:
    provider: str
    model: str
    input_tokens: int
    output_tokens: int
    estimated_cost_usd: float


class ModelGateway:
    """Keeps model selection, attribution and data policy outside process nodes."""

    def analyze_impact(
        self, domain: str, request: ChangeRequest, sources: list[SourceDocument]
    ) -> tuple[ImpactFinding, ModelUsage]:
        if os.getenv("MODEL_PROVIDER", "deterministic") == "ollama":
            return self._ollama_impact(domain, request, sources)
        return self._deterministic_impact(domain, request, sources)

    @staticmethod
    def _deterministic_impact(
        domain: str, request: ChangeRequest, sources: list[SourceDocument]
    ) -> tuple[ImpactFinding, ModelUsage]:
        source = sources[0]
        summaries = {
            "risk": "Control evidence and residual-risk ownership must be reconfirmed for the revised retention path.",
            "operations": "The operating procedure, reviewer responsibilities and service-level clock require a versioned update.",
            "technology": "Access control, lineage and deletion obligations must be verified before implementation.",
        }
        finding = ImpactFinding(
            domain=domain,
            summary=f"{summaries[domain]} Requested change: {request.requested_change}",
            severity="high" if domain == "technology" else "medium",
            citations=[Citation(source_id=source.source_id, version=source.version, excerpt=source.content[:180])],
        )
        return finding, ModelUsage("deterministic", "fixture-v1", 0, 0, 0.0)

    @staticmethod
    def _ollama_impact(
        domain: str, request: ChangeRequest, sources: list[SourceDocument]
    ) -> tuple[ImpactFinding, ModelUsage]:
        from langchain_ollama import ChatOllama

        model_name = os.getenv("OLLAMA_CHAT_MODEL", "qwen2.5:7b")
        model = ChatOllama(model=model_name, temperature=0).with_structured_output(ImpactFinding)
        source_text = "\n".join(f"[{item.source_id}@{item.version}] {item.content}" for item in sources)
        finding = model.invoke(
            "You are a bounded internal banking impact analyst. Return only supported findings with citations.\n"
            f"Domain: {domain}\nRequest: {request.model_dump_json()}\nApproved sources:\n{source_text}"
        )
        return finding, ModelUsage("ollama", model_name, 0, 0, 0.0)
