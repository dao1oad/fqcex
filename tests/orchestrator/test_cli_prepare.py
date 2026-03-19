from pathlib import Path
import json
import subprocess
import sys


def test_cli_prepare_outputs_worktree_branch_and_dispatch_payload(tmp_path: Path) -> None:
    approval_path = tmp_path / "approval_bundle.json"
    issues_path = tmp_path / "issues.json"
    issues_path.write_text(
        json.dumps(
            [
                {
                    "issue_id": 29,
                    "issue_title": "Quantity normalization",
                    "tracking_issue_id": 11,
                    "state": "open",
                    "type_label": "type/task",
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
            "29",
            "--issues-path",
            str(issues_path),
            "--approval-path",
            str(approval_path),
        ],
        capture_output=True,
        text=True,
        check=False,
        cwd=repo_root,
    )

    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["branch"] == "codex/issue-29-quantity-normalization"
    assert payload["worktree_path"].endswith("issue-29-quantity-normalization")
    assert payload["owner_payload"]["approval_bundle_id"]
    assert payload["owner_payload"]["model"] == "gpt-5.4"


def test_cli_prepare_rejects_issue_out_of_approval_scope(tmp_path: Path) -> None:
    approval_path = tmp_path / "approval_bundle.json"
    issues_path = tmp_path / "issues.json"
    issues_path.write_text(
        json.dumps(
            [
                {
                    "issue_id": 34,
                    "issue_title": "Out of scope",
                    "tracking_issue_id": 11,
                    "state": "open",
                    "type_label": "type/task",
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
            "34",
            "--issues-path",
            str(issues_path),
            "--approval-path",
            str(approval_path),
        ],
        capture_output=True,
        text=True,
        check=False,
        cwd=repo_root,
    )

    assert result.returncode == 1
    assert "out of approved scope" in result.stdout


def test_cli_prepare_rejects_closed_issue(tmp_path: Path) -> None:
    approval_path = tmp_path / "approval_bundle.json"
    issues_path = tmp_path / "issues.json"
    issues_path.write_text(
        json.dumps(
            [
                {
                    "issue_id": 29,
                    "issue_title": "Done",
                    "tracking_issue_id": 11,
                    "state": "closed",
                    "type_label": "type/task",
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
            "29",
            "--issues-path",
            str(issues_path),
            "--approval-path",
            str(approval_path),
        ],
        capture_output=True,
        text=True,
        check=False,
        cwd=repo_root,
    )

    assert result.returncode == 1
    assert "issue not claimable" in result.stdout
