from pathlib import Path

from perp_platform.orchestrator.models import ApprovalBundle
from perp_platform.orchestrator.runtime_state import (
    load_approval_bundle,
    save_approval_bundle,
)


def test_approval_bundle_round_trip(tmp_path: Path) -> None:
    path = tmp_path / "approval_bundle.json"
    bundle = ApprovalBundle(
        bundle_id="exec-2026-03-19-001",
        approved_by_user=True,
        approved_at="2026-03-19T10:00:00+08:00",
        scope_label="issues_30_to_33",
        issue_start=30,
        issue_end=33,
        execution_mode="proceed_with_recommended_defaults",
        issue_parallelism=1,
        write_agents_per_issue=1,
        read_only_sidecars_per_issue=2,
        merge_policy="auto_merge_main",
        close_policy="auto_close_child_and_update_tracking",
        reporting_policy="issue_completion_or_blocked_only",
        pause_only_on=("sibling_issue_required",),
        recommended_defaults=("recommended",),
        model="gpt-5.4",
        reasoning_effort="xhigh",
    )

    save_approval_bundle(path, bundle)
    loaded = load_approval_bundle(path)

    assert loaded.bundle_id == "exec-2026-03-19-001"
    assert loaded.issue_start == 30
    assert loaded.model == "gpt-5.4"
