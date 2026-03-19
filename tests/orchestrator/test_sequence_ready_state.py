from perp_platform.orchestrator.models import IssueSnapshot
from perp_platform.orchestrator.sequence import select_next_ready_snapshot


def test_select_next_ready_issue_rejects_other_assignee() -> None:
    snapshots = [
        IssueSnapshot(
            issue_id=30,
            issue_title="Doc constraints",
            tracking_issue_id=11,
            epic_issue_id=2,
            sequence_index=0,
            state="open",
            type_label="type/task",
            phase_labels=("phase/1",),
            area_labels=("area/architecture",),
            assignees=("someone-else",),
            body="",
        )
    ]

    selected = select_next_ready_snapshot(
        snapshots,
        closed_issue_ids=set(),
        current_operator="dao1oad",
    )

    assert selected is None


def test_select_next_ready_issue_rejects_invalid_type_label() -> None:
    snapshots = [
        IssueSnapshot(
            issue_id=30,
            issue_title="Tracking issue",
            tracking_issue_id=11,
            epic_issue_id=2,
            sequence_index=0,
            state="open",
            type_label="type/tracking",
            phase_labels=(),
            area_labels=(),
            assignees=(),
            body="",
        )
    ]

    selected = select_next_ready_snapshot(
        snapshots,
        closed_issue_ids=set(),
        current_operator="dao1oad",
    )

    assert selected is None


def test_select_next_ready_issue_prefers_earlier_global_sequence_across_trackings() -> None:
    snapshots = [
        IssueSnapshot(
            issue_id=31,
            issue_title="Later tracking child",
            tracking_issue_id=12,
            epic_issue_id=2,
            sequence_index=3,
            state="open",
            type_label="type/task",
            phase_labels=("phase/1",),
            area_labels=("area/runtime",),
            assignees=("dao1oad",),
            body="",
        ),
        IssueSnapshot(
            issue_id=30,
            issue_title="Earlier tracking child",
            tracking_issue_id=11,
            epic_issue_id=2,
            sequence_index=2,
            state="open",
            type_label="type/task",
            phase_labels=("phase/1",),
            area_labels=("area/architecture",),
            assignees=("dao1oad",),
            body="",
        ),
    ]

    selected = select_next_ready_snapshot(
        snapshots,
        closed_issue_ids=set(),
        current_operator="dao1oad",
    )

    assert selected is not None
    assert selected.issue_id == 30
