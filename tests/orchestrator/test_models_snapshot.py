from perp_platform.orchestrator.models import IssueSnapshot


def test_issue_snapshot_keeps_sequence_and_labels() -> None:
    snapshot = IssueSnapshot(
        issue_id=30,
        issue_title="Doc constraints",
        tracking_issue_id=11,
        epic_issue_id=2,
        sequence_index=2,
        state="open",
        type_label="type/task",
        phase_labels=("phase/1",),
        area_labels=("area/architecture",),
        assignees=("dao1oad",),
        body="body",
    )

    assert snapshot.sequence_index == 2
    assert snapshot.type_label == "type/task"
    assert snapshot.assignees == ("dao1oad",)
