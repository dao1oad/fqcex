from perp_platform.orchestrator.models import OrchestratorState, WorkItem
from perp_platform.orchestrator.sequence import select_next_ready_issue


def test_select_next_ready_issue_uses_first_open_child_after_closed_siblings() -> None:
    work_items = [
        WorkItem(
            issue_id=28,
            issue_title="closed",
            tracking_issue_id=11,
            status=OrchestratorState.CLOSED,
        ),
        WorkItem(issue_id=29, issue_title="ready", tracking_issue_id=11),
        WorkItem(issue_id=30, issue_title="blocked-by-order", tracking_issue_id=11),
    ]

    selected = select_next_ready_issue(work_items, closed_issue_ids={28})

    assert selected is not None
    assert selected.issue_id == 29
