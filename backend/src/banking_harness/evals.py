"""Deterministic in-run and release evaluation primitives."""

from __future__ import annotations

from .knowledge import SourceDocument
from .models import ChangeRequest, EvalResult, ImpactFinding


def evaluate_case(
    request: ChangeRequest,
    findings: list[ImpactFinding],
    missing: list[str],
    sources: list[SourceDocument],
) -> list[EvalResult]:
    required_domains = {"risk", "operations", "technology"}
    returned_domains = {finding.domain for finding in findings}
    citation_count = sum(len(finding.citations) for finding in findings)
    valid_source_refs = {(source.source_id, source.version) for source in sources}
    citations = [citation for finding in findings for citation in finding.citations]
    citations_valid = bool(citations) and all(
        (citation.source_id, citation.version) in valid_source_refs for citation in citations
    )
    source_linked = bool(request.existing_item_id)
    source_linkage_detail = (
        "Change case is linked to an authoritative current item."
        if source_linked
        else "Not applicable: this request creates a new implementation."
    )
    checks = [
        EvalResult(
            name="required_evidence",
            score=1.0 if not missing else 0.0,
            threshold=1.0,
            passed=not missing,
            detail="All mandatory evidence references supplied."
            if not missing
            else f"Missing: {', '.join(missing)}",
        ),
        EvalResult(
            name="impact_coverage",
            score=len(returned_domains & required_domains) / 3,
            threshold=1.0,
            passed=returned_domains == required_domains,
            detail=f"Covered {len(returned_domains)}/3 required domains.",
        ),
        EvalResult(
            name="citation_coverage",
            score=min(citation_count / 3, 1.0),
            threshold=1.0,
            passed=citation_count >= 3,
            detail=f"{citation_count} cited impact findings.",
        ),
        EvalResult(
            name="citation_integrity",
            score=1.0 if citations_valid else 0.0,
            threshold=1.0,
            passed=citations_valid,
            detail="Every citation resolves to a retrieved source and version."
            if citations_valid
            else "One or more citations do not resolve to retrieved evidence.",
        ),
        EvalResult(
            name="source_linkage",
            score=1.0,
            threshold=1.0,
            passed=True,
            detail=source_linkage_detail,
        ),
    ]
    return checks


def release_gate(results: list[EvalResult]) -> bool:
    """A release/run passes only when every mandatory evaluator passes."""

    return bool(results) and all(result.passed and result.score >= result.threshold for result in results)
