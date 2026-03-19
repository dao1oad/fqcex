from pathlib import Path
import json
import subprocess
import sys


def test_cli_next_prints_unique_ready_issue(tmp_path: Path) -> None:
    issues_path = tmp_path / "issues.json"
    issues_path.write_text(
        json.dumps(
            [
                {
                    "issue_id": 28,
                    "issue_title": "done",
                    "tracking_issue_id": 11,
                    "state": "closed",
                    "type_label": "type/task",
                },
                {
                    "issue_id": 29,
                    "issue_title": "ready",
                    "tracking_issue_id": 11,
                    "state": "open",
                    "type_label": "type/task",
                },
                {
                    "issue_id": 30,
                    "issue_title": "later",
                    "tracking_issue_id": 11,
                    "state": "open",
                    "type_label": "type/task",
                },
            ]
        ),
        encoding="utf-8",
    )
    repo_root = Path(__file__).resolve().parents[2]

    result = subprocess.run(
        [
            sys.executable,
            "scripts/issue_orchestrator.py",
            "next",
            "--issues-path",
            str(issues_path),
        ],
        capture_output=True,
        text=True,
        check=False,
        cwd=repo_root,
    )

    assert result.returncode == 0
    assert "29" in result.stdout
    assert "ready" in result.stdout


def test_cli_claim_persists_claimed_state(tmp_path: Path) -> None:
    issues_path = tmp_path / "issues.json"
    issues_path.write_text(
        json.dumps(
            [
                {
                    "issue_id": 29,
                    "issue_title": "ready",
                    "tracking_issue_id": 11,
                    "state": "open",
                    "type_label": "type/task",
                }
            ]
        ),
        encoding="utf-8",
    )
    state_path = tmp_path / "state.json"
    repo_root = Path(__file__).resolve().parents[2]

    result = subprocess.run(
        [
            sys.executable,
            "scripts/issue_orchestrator.py",
            "claim",
            "29",
            "--issues-path",
            str(issues_path),
            "--state-path",
            str(state_path),
        ],
        capture_output=True,
        text=True,
        check=False,
        cwd=repo_root,
    )

    assert result.returncode == 0
    payload = json.loads(state_path.read_text(encoding="utf-8"))
    assert payload["issue_id"] == 29
    assert payload["status"] == "claimed"


def test_cli_claim_rejects_closed_issue(tmp_path: Path) -> None:
    issues_path = tmp_path / "issues.json"
    issues_path.write_text(
        json.dumps(
            [
                {
                    "issue_id": 29,
                    "issue_title": "done",
                    "tracking_issue_id": 11,
                    "state": "closed",
                    "type_label": "type/task",
                }
            ]
        ),
        encoding="utf-8",
    )
    state_path = tmp_path / "state.json"
    repo_root = Path(__file__).resolve().parents[2]

    result = subprocess.run(
        [
            sys.executable,
            "scripts/issue_orchestrator.py",
            "claim",
            "29",
            "--issues-path",
            str(issues_path),
            "--state-path",
            str(state_path),
        ],
        capture_output=True,
        text=True,
        check=False,
        cwd=repo_root,
    )

    assert result.returncode == 1
    assert "issue not claimable" in result.stdout
