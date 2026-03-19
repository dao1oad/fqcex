"""GitHub state helpers for the issue orchestrator."""

import json
from pathlib import Path

from .models import OrchestratorState, WorkItem


def load_task_work_items(path: Path) -> tuple[list[WorkItem], set[int]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    work_items: list[WorkItem] = []
    closed_issue_ids: set[int] = set()

    for issue in payload:
        if issue.get("type_label") != "type/task":
            continue

        status = (
            OrchestratorState.CLOSED
            if issue["state"] == "closed"
            else OrchestratorState.READY
        )
        work_item = WorkItem(
            issue_id=issue["issue_id"],
            issue_title=issue["issue_title"],
            tracking_issue_id=issue["tracking_issue_id"],
            status=status,
        )
        work_items.append(work_item)

        if issue["state"] == "closed":
            closed_issue_ids.add(issue["issue_id"])

    return work_items, closed_issue_ids


def find_task_work_item(path: Path, issue_id: int) -> WorkItem | None:
    work_items, _ = load_task_work_items(path)

    for work_item in work_items:
        if work_item.issue_id == issue_id:
            return work_item

    return None


def find_claimable_task_work_item(path: Path, issue_id: int) -> WorkItem | None:
    work_item = find_task_work_item(path, issue_id)

    if work_item is None:
        return None

    if work_item.status is OrchestratorState.CLOSED:
        return None

    return work_item
