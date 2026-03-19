"""GitHub state helpers for the issue orchestrator."""

import subprocess
import json
from pathlib import Path

from .gh_sync import normalize_github_issues
from .models import IssueSnapshot, OrchestratorState, WorkItem
from .sequence import parse_issue_hierarchy, select_next_ready_snapshot


def sync_github_issues(
    *,
    hierarchy_path: Path,
    output_path: Path,
    gh_json_path: Path | None = None,
) -> list[dict[str, object]]:
    hierarchy = parse_issue_hierarchy(hierarchy_path.read_text(encoding="utf-8"))
    if gh_json_path is not None:
        issues = json.loads(gh_json_path.read_text(encoding="utf-8"))
    else:
        result = subprocess.run(
            [
                "gh",
                "issue",
                "list",
                "--limit",
                "200",
                "--state",
                "all",
                "--json",
                "number,title,state,labels,assignees,body",
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        issues = json.loads(result.stdout)

    normalized = normalize_github_issues(issues, hierarchy)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(normalized, indent=2), encoding="utf-8")
    return normalized


def load_issue_snapshots(path: Path) -> list[IssueSnapshot]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    snapshots: list[IssueSnapshot] = []

    for issue in payload:
        snapshots.append(
            IssueSnapshot(
                issue_id=issue["issue_id"],
                issue_title=issue["issue_title"],
                tracking_issue_id=issue.get("tracking_issue_id", 0),
                epic_issue_id=issue.get("epic_issue_id", 0),
                sequence_index=issue.get("sequence_index", 0),
                state=issue["state"],
                type_label=issue.get("type_label", ""),
                phase_labels=tuple(issue.get("phase_labels", [])),
                area_labels=tuple(issue.get("area_labels", [])),
                assignees=tuple(issue.get("assignees", [])),
                body=issue.get("body", ""),
            )
        )

    return snapshots


def snapshot_to_work_item(snapshot: IssueSnapshot) -> WorkItem:
    status = OrchestratorState.CLOSED if snapshot.state == "closed" else OrchestratorState.READY
    return WorkItem(
        issue_id=snapshot.issue_id,
        issue_title=snapshot.issue_title,
        tracking_issue_id=snapshot.tracking_issue_id,
        status=status,
    )


def load_task_work_items(path: Path) -> tuple[list[WorkItem], set[int]]:
    snapshots = load_issue_snapshots(path)
    work_items: list[WorkItem] = []
    closed_issue_ids: set[int] = set()

    for snapshot in snapshots:
        if snapshot.type_label != "type/task":
            continue

        work_item = snapshot_to_work_item(snapshot)
        work_items.append(work_item)

        if snapshot.state == "closed":
            closed_issue_ids.add(snapshot.issue_id)

    return work_items, closed_issue_ids


def find_issue_snapshot(path: Path, issue_id: int) -> IssueSnapshot | None:
    snapshots = load_issue_snapshots(path)

    for snapshot in snapshots:
        if snapshot.issue_id == issue_id:
            return snapshot

    return None


def find_task_work_item(path: Path, issue_id: int) -> WorkItem | None:
    work_items, _ = load_task_work_items(path)

    for work_item in work_items:
        if work_item.issue_id == issue_id:
            return work_item

    return None


def find_claimable_issue_snapshot(
    path: Path, issue_id: int, current_operator: str
) -> IssueSnapshot | None:
    snapshots = load_issue_snapshots(path)
    closed_issue_ids = {
        snapshot.issue_id for snapshot in snapshots if snapshot.state == "closed"
    }
    selected = select_next_ready_snapshot(
        snapshots,
        closed_issue_ids=closed_issue_ids,
        current_operator=current_operator,
    )
    if selected is None or selected.issue_id != issue_id:
        return None

    return selected
