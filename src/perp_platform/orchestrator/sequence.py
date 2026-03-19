"""Issue sequencing rules for the issue orchestrator."""

from .models import WorkItem


def select_next_ready_issue(
    work_items: list[WorkItem], closed_issue_ids: set[int]
) -> WorkItem | None:
    for work_item in work_items:
        if work_item.issue_id in closed_issue_ids:
            continue
        return work_item

    return None
