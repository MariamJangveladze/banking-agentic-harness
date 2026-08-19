from test_graph import complete_request

from banking_harness.evals import evaluate_case, release_gate
from banking_harness.models import Citation, ImpactFinding


def test_release_gate_requires_all_domains_and_citations() -> None:
    citation = Citation(source_id="OPS-PROC-014", version="3.2", excerpt="Controlled source")
    findings = [ImpactFinding(domain=domain, summary="Supported finding", severity="medium", citations=[citation]) for domain in ("risk", "operations", "technology")]
    results = evaluate_case(complete_request(), findings, [])
    assert release_gate(results)


def test_release_gate_fails_without_technology_finding() -> None:
    citation = Citation(source_id="OPS-PROC-014", version="3.2", excerpt="Controlled source")
    findings = [ImpactFinding(domain=domain, summary="Supported finding", severity="medium", citations=[citation]) for domain in ("risk", "operations")]
    results = evaluate_case(complete_request(), findings, [])
    assert not release_gate(results)
