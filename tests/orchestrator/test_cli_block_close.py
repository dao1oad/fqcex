from pathlib import Path
import json
import subprocess
import sys


def test_cli_block_records_reason(tmp_path: Path) -> None:
    state_path = tmp_path / "state.json"
    state_path.write_text(
        json.dumps(
            {
                "issue_id": 29,
                "issue_title": "Quantity",
                "tracking_issue_id": 11,
                "status": "claimed",
                "owner_agent_id": "agent-1",
            }
        ),
        encoding="utf-8",
    )
    repo_root = Path(__file__).resolve().parents[2]

    result = subprocess.run(
        [
            sys.executable,
            "scripts/issue_orchestrator.py",
            "block",
            "29",
            "--state-path",
            str(state_path),
            "--reason",
            "needs sibling issue",
        ],
        capture_output=True,
        text=True,
        check=False,
        cwd=repo_root,
    )

    assert result.returncode == 0
    payload = json.loads(state_path.read_text(encoding="utf-8"))
    assert payload["status"] == "blocked"
    assert payload["blocker_reason"] == "needs sibling issue"


def test_cli_close_clears_runtime_state(tmp_path: Path) -> None:
    state_path = tmp_path / "state.json"
    state_path.write_text(
        json.dumps(
            {
                "issue_id": 29,
                "issue_title": "Quantity",
                "tracking_issue_id": 11,
                "status": "merged",
                "owner_agent_id": "agent-1",
            }
        ),
        encoding="utf-8",
    )
    repo_root = Path(__file__).resolve().parents[2]

    result = subprocess.run(
        [
            sys.executable,
            "scripts/issue_orchestrator.py",
            "close",
            "29",
            "--state-path",
            str(state_path),
        ],
        capture_output=True,
        text=True,
        check=False,
        cwd=repo_root,
    )

    assert result.returncode == 0
    assert not state_path.exists()
