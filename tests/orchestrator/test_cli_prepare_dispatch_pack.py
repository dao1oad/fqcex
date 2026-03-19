from pathlib import Path
import json
import subprocess
import sys


def expected_worktree_path(repo_root: Path, issue_slug: str) -> str:
    result = subprocess.run(
        ["git", "rev-parse", "--git-common-dir"],
        capture_output=True,
        text=True,
        check=True,
        cwd=repo_root,
    )
    common_dir = Path(result.stdout.strip())
    if not common_dir.is_absolute():
        common_dir = (repo_root / common_dir).resolve()
    return str(common_dir.parent / ".worktrees" / issue_slug)


def test_prepare_outputs_execution_context_constraints_and_prompt(
    tmp_path: Path,
) -> None:
    approval_path = tmp_path / "approval_bundle.json"
    issues_path = tmp_path / "issues.json"
    issues_path.write_text(
        json.dumps(
            [
                {
                    "issue_id": 30,
                    "issue_title": "Doc constraints",
                    "tracking_issue_id": 11,
                    "epic_issue_id": 2,
                    "sequence_index": 2,
                    "state": "open",
                    "type_label": "type/task",
                    "phase_labels": ["phase/1"],
                    "area_labels": ["area/architecture"],
                    "assignees": ["dao1oad"],
                    "body": "Tracking Parent: #11\nEpic: #2",
                }
            ]
        ),
        encoding="utf-8",
    )
    repo_root = Path(__file__).resolve().parents[2]

    subprocess.run(
        [
            sys.executable,
            "scripts/issue_orchestrator.py",
            "approval",
            "create",
            "--issue-start",
            "30",
            "--issue-end",
            "33",
            "--approval-path",
            str(approval_path),
        ],
        capture_output=True,
        text=True,
        check=True,
        cwd=repo_root,
    )

    result = subprocess.run(
        [
            sys.executable,
            "scripts/issue_orchestrator.py",
            "prepare",
            "30",
            "--issues-path",
            str(issues_path),
            "--approval-path",
            str(approval_path),
            "--operator",
            "dao1oad",
        ],
        capture_output=True,
        text=True,
        check=False,
        cwd=repo_root,
    )

    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["execution_context"]["issue_id"] == 30
    assert payload["execution_context"]["tracking_issue_id"] == 11
    assert payload["worktree_path"] == expected_worktree_path(
        repo_root, "issue-30-doc-constraints"
    )
    assert payload["constraints"]["escalation_triggers"]
    assert "Do not ask the user for design confirmation." in payload["subagent_prompt"]


def test_prepare_rejects_issue_when_earlier_sequence_item_is_still_open(
    tmp_path: Path,
) -> None:
    approval_path = tmp_path / "approval_bundle.json"
    issues_path = tmp_path / "issues.json"
    issues_path.write_text(
        json.dumps(
            [
                {
                    "issue_id": 29,
                    "issue_title": "Earlier task",
                    "tracking_issue_id": 11,
                    "epic_issue_id": 2,
                    "sequence_index": 0,
                    "state": "open",
                    "type_label": "type/task",
                    "phase_labels": ["phase/1"],
                    "area_labels": ["area/architecture"],
                    "assignees": ["dao1oad"],
                    "body": "Tracking Parent: #11\nEpic: #2",
                },
                {
                    "issue_id": 30,
                    "issue_title": "Later task",
                    "tracking_issue_id": 11,
                    "epic_issue_id": 2,
                    "sequence_index": 1,
                    "state": "open",
                    "type_label": "type/task",
                    "phase_labels": ["phase/1"],
                    "area_labels": ["area/architecture"],
                    "assignees": ["dao1oad"],
                    "body": "Tracking Parent: #11\nEpic: #2",
                },
            ]
        ),
        encoding="utf-8",
    )
    repo_root = Path(__file__).resolve().parents[2]

    subprocess.run(
        [
            sys.executable,
            "scripts/issue_orchestrator.py",
            "approval",
            "create",
            "--issue-start",
            "29",
            "--issue-end",
            "33",
            "--approval-path",
            str(approval_path),
        ],
        capture_output=True,
        text=True,
        check=True,
        cwd=repo_root,
    )

    result = subprocess.run(
        [
            sys.executable,
            "scripts/issue_orchestrator.py",
            "prepare",
            "30",
            "--issues-path",
            str(issues_path),
            "--approval-path",
            str(approval_path),
            "--operator",
            "dao1oad",
        ],
        capture_output=True,
        text=True,
        check=False,
        cwd=repo_root,
    )

    assert result.returncode == 1
    assert "issue not claimable" in result.stdout
