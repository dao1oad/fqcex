"""Normalize GitHub issue metadata for local orchestrator snapshots."""


def normalize_github_issues(
    issues: list[dict[str, object]], hierarchy: dict[int, dict[str, int]]
) -> list[dict[str, object]]:
    normalized: list[dict[str, object]] = []

    for issue in issues:
        issue_id = int(issue["number"])
        labels = [label["name"] for label in issue.get("labels", [])]
        type_label = next((label for label in labels if label.startswith("type/")), "")
        state = str(issue["state"]).lower()
        hierarchy_entry = hierarchy.get(issue_id)
        if hierarchy_entry is None:
            if type_label == "type/task" and state == "open":
                raise ValueError(
                    "open task issue missing from ISSUE_HIERARCHY.md: "
                    f"#{issue_id} {issue['title']}"
                )
            continue

        phase_labels = [label for label in labels if label.startswith("phase/")]
        area_labels = [label for label in labels if label.startswith("area/")]
        assignees = [assignee["login"] for assignee in issue.get("assignees", [])]

        normalized.append(
            {
                "issue_id": issue_id,
                "issue_title": issue["title"],
                "tracking_issue_id": hierarchy_entry["tracking_issue_id"],
                "epic_issue_id": hierarchy_entry["epic_issue_id"],
                "sequence_index": hierarchy_entry["sequence_index"],
                "state": state,
                "type_label": type_label,
                "phase_labels": phase_labels,
                "area_labels": area_labels,
                "assignees": assignees,
                "body": issue.get("body", ""),
            }
        )

    return normalized
