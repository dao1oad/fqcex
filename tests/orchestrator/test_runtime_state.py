from pathlib import Path

from perp_platform.orchestrator.models import OrchestratorState, WorkItem
from perp_platform.orchestrator.runtime_state import load_state, save_state


def test_runtime_state_round_trip(tmp_path: Path) -> None:
    path = tmp_path / "state.json"
    work_item = WorkItem(
        issue_id=29,
        issue_title="issue",
        tracking_issue_id=11,
        status=OrchestratorState.CLAIMED,
    )

    save_state(path, work_item)
    loaded = load_state(path)

    assert loaded.issue_id == 29
    assert loaded.status is OrchestratorState.CLAIMED
