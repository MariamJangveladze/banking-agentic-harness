"""Deterministic in-run and release evaluation primitives."""

from __future__ import annotations

from .models import ChangeRequest, EvalResult, ImpactFinding


def evaluate_case(request: ChangeRequest, findings: list[ImpactFinding], missing: list[str]) -> list[EvalResult]:
    required_domains = {"risk", "operations", "technology"}
    returned_domains = {finding.domain for finding in findings}
    citation_count = sum(len(finding.citations) for finding in findings)
    checks = [
        EvalResult(name="required_evidence", score=1.0 if not missing else 0.0, threshold=1.0, passed=not missing, detail="All mandatory evidence references supplied." if not missing else f"Missing: {', '.join(missing)}"),
        EvalResult(name="impact_coverage", score=len(returned_domains & required_domains) / 3, threshold=1.0, passed=returned_domains == required_domains, detail=f"Covered {len(returned_domains)}/3 required domains."),
        EvalResult(name="citation_coverage", score=min(citation_count / 3, 1.0), threshold=1.0, passed=citation_count >= 3, detail=f"{citation_count} cited impact findings."),
        EvalResult(name="source_linkage", score=1.0 if request.existing_item_id else 0.0, threshold=1.0, passed=bool(request.existing_item_id), detail="Change case is linked to an authoritative current item."),
    ]
    return checks


def release_gate(results: list[EvalResult]) -> bool:
    """A release/run passes only when every mandatory evaluator passes."""

    return bool(results) and all(result.passed and result.score >= result.threshold for result in results)
