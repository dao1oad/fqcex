"""Issue sequencing rules for the issue orchestrator."""

import re

from .models import IssueSnapshot, WorkItem


ISSUE_REF_PATTERN = re.compile(r"#(?P<issue_id>\d+)")


def parse_issue_hierarchy(content: str) -> dict[int, dict[str, int]]:
    hierarchy: dict[int, dict[str, int]] = {}
    current_epic_id: int | None = None
    current_tracking_id: int | None = None
    current_sequence_index = -1

    for raw_line in content.splitlines():
        line = raw_line.rstrip()
        match = ISSUE_REF_PATTERN.search(line)
        if match is None:
            continue

        issue_id = int(match.group("issue_id"))
        stripped = line.lstrip()
        indent = len(line) - len(stripped)

        if "[Epic]" in line:
            current_epic_id = issue_id
            current_tracking_id = None
            continue

        if "[Tracking]" in line:
            current_tracking_id = issue_id
            continue

        if indent >= 4 and current_epic_id is not None and current_tracking_id is not None:
            current_sequence_index += 1
            hierarchy[issue_id] = {
                "tracking_issue_id": current_tracking_id,
                "epic_issue_id": current_epic_id,
                "sequence_index": current_sequence_index,
            }

    return hierarchy


def select_next_ready_issue(
    work_items: list[WorkItem], closed_issue_ids: set[int]
) -> WorkItem | None:
    for work_item in work_items:
        if work_item.issue_id in closed_issue_ids:
            continue
        return work_item

    return None


def select_next_ready_snapshot(
    snapshots: list[IssueSnapshot],
    closed_issue_ids: set[int],
    current_operator: str,
) -> IssueSnapshot | None:
    ordered_snapshots = sorted(snapshots, key=lambda snapshot: snapshot.sequence_index)

    for snapshot in ordered_snapshots:
        if snapshot.type_label != "type/task":
            continue
        if snapshot.state != "open":
            continue
        if snapshot.assignees and current_operator not in snapshot.assignees:
            continue
        if any(
            sibling.sequence_index < snapshot.sequence_index
            and sibling.issue_id not in closed_issue_ids
            and sibling.state != "closed"
            for sibling in ordered_snapshots
        ):
            continue
        return snapshot

    return None
