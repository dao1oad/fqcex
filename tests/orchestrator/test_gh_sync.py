from perp_platform.orchestrator.gh_sync import normalize_github_issues


def test_normalize_github_issues_merges_hierarchy_and_issue_metadata() -> None:
    issues = [
        {
            "number": 30,
            "title": "Doc constraints",
            "state": "OPEN",
            "labels": [{"name": "type/task"}, {"name": "phase/1"}],
            "assignees": [{"login": "dao1oad"}],
            "body": "Tracking Parent: #11\nEpic: #2",
        }
    ]
    hierarchy = {
        30: {
            "tracking_issue_id": 11,
            "epic_issue_id": 2,
            "sequence_index": 2,
        }
    }

    normalized = normalize_github_issues(issues, hierarchy)

    assert normalized[0]["issue_id"] == 30
    assert normalized[0]["tracking_issue_id"] == 11
    assert normalized[0]["epic_issue_id"] == 2
    assert normalized[0]["type_label"] == "type/task"
    assert normalized[0]["phase_labels"] == ["phase/1"]


def test_normalize_github_issues_rejects_open_task_missing_from_hierarchy() -> None:
    issues = [
        {
            "number": 89,
            "title": "Review governance",
            "state": "OPEN",
            "labels": [{"name": "type/task"}, {"name": "phase/1"}],
            "assignees": [{"login": "dao1oad"}],
            "body": "Tracking Parent: #79\nEpic: #2",
        }
    ]

    try:
        normalize_github_issues(issues, {})
    except ValueError as exc:
        assert "open task issue missing from ISSUE_HIERARCHY.md" in str(exc)
        assert "#89" in str(exc)
    else:
        raise AssertionError("expected open hierarchy drift to fail closed")
