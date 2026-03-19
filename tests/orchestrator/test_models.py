from perp_platform.orchestrator.models import AgentRole, OrchestratorState, WorkItem


def test_work_item_defaults() -> None:
    work_item = WorkItem(issue_id=29, issue_title="test", tracking_issue_id=11)

    assert work_item.issue_id == 29
    assert work_item.status is OrchestratorState.READY
    assert work_item.owner_agent_id is None
    assert AgentRole.OWNER.value == "owner"
