from pathlib import Path
import json
import subprocess
import sys


def test_claim_rejects_issue_when_earlier_sequence_item_is_still_open(
    tmp_path: Path,
) -> None:
    issues_path = tmp_path / "issues.json"
    state_path = tmp_path / "state.json"
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

    result = subprocess.run(
        [
            sys.executable,
            "scripts/issue_orchestrator.py",
            "claim",
            "30",
            "--issues-path",
            str(issues_path),
            "--state-path",
            str(state_path),
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
