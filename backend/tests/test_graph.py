from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command

from banking_harness.graph import build_product_change_graph, new_case_input
from banking_harness.models import CaseStatus, ChangeRequest


def complete_request() -> ChangeRequest:
    return ChangeRequest(
        title="Digital archive retention process",
        owner="Nino Beridze",
        business_purpose="Align the internal archive process with updated retention obligations.",
        requested_change="Update reviewer responsibilities and the deletion-control evidence path.",
        existing_item_id="OPS-PROC-014",
        risk_reference="RISK-2026-44",
        legal_reference="LEGAL-2026-18",
        infosec_reference="INFOSEC-2026-09",
        related_department_reference="OPS-2026-31",
    )


def test_complete_case_pauses_for_product_support_and_resumes() -> None:
    graph = build_product_change_graph(checkpointer=InMemorySaver())
    state = new_case_input(complete_request(), "CASE-TEST-001")
    config = {"configurable": {"thread_id": state["case_id"]}}

    paused = graph.invoke(state, config)
    assert paused["status"] == CaseStatus.RUNNING.value
    assert len(paused["findings"]) == 3
    assert all(item["passed"] for item in paused["eval_results"])
    assert paused["__interrupt__"][0].value["kind"] == "product_support_approval"

    completed = graph.invoke(Command(resume={"decision": "approve", "reviewer": "Product Support", "comment": "Evidence verified."}), config)
    assert completed["status"] == CaseStatus.APPROVED.value
    assert completed["controlled_action"]["mode"] == "SIMULATED"


def test_new_implementation_can_reach_product_support_approval() -> None:
    graph = build_product_change_graph(checkpointer=InMemorySaver())
    request = complete_request().model_copy(update={"existing_item_id": None})
    state = new_case_input(request, "CASE-TEST-NEW")
    config = {"configurable": {"thread_id": state["case_id"]}}

    paused = graph.invoke(state, config)

    assert paused["classification"] == "NEW_IMPLEMENTATION"
    assert all(item["passed"] for item in paused["eval_results"])
    source_gate = next(item for item in paused["eval_results"] if item["name"] == "source_linkage")
    assert source_gate["detail"].startswith("Not applicable")
    assert paused["__interrupt__"][0].value["kind"] == "product_support_approval"


def test_missing_evidence_stops_before_agent_execution() -> None:
    graph = build_product_change_graph(checkpointer=InMemorySaver())
    request = complete_request().model_copy(update={"legal_reference": None})
    state = new_case_input(request, "CASE-TEST-002")

    result = graph.invoke(state, {"configurable": {"thread_id": state["case_id"]}})
    assert result["status"] == CaseStatus.NEEDS_INFORMATION.value
    assert result["findings"] == []
    assert "legal_reference" in result["missing_evidence"]
