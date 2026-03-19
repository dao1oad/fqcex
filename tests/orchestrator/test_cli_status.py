from pathlib import Path
import subprocess
import sys


def test_issue_orchestrator_status_reads_runtime_state(tmp_path: Path) -> None:
    state_path = tmp_path / "state.json"
    state_path.write_text(
        '{"issue_id": 29, "issue_title": "Quantity", "tracking_issue_id": 11, "status": "claimed", "owner_agent_id": null}',
        encoding="utf-8",
    )

    result = subprocess.run(
        [sys.executable, "scripts/issue_orchestrator.py", "status", "--state-path", str(state_path)],
        capture_output=True,
        text=True,
        check=False,
        cwd=Path(__file__).resolve().parents[2],
    )

    assert result.returncode == 0
    assert "29" in result.stdout
    assert "claimed" in result.stdout
