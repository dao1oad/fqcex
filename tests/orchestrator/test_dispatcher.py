from perp_platform.orchestrator.dispatcher import build_owner_dispatch_payload
from perp_platform.orchestrator.models import ApprovalBundle, WorkItem


def test_owner_dispatch_payload_contains_model_and_scope() -> None:
    work_item = WorkItem(issue_id=29, issue_title="Quantity", tracking_issue_id=11)
    approval_bundle = ApprovalBundle(
        bundle_id="exec-2026-03-19-001",
        approved_by_user=True,
        approved_at="2026-03-19T10:00:00+08:00",
        scope_label="issues_29_to_33",
        issue_start=29,
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

    payload = build_owner_dispatch_payload(
        work_item=work_item,
        approval_bundle=approval_bundle,
        worktree_path="D:/fqcex/.worktrees/issue-29",
        allowed_files=["src/perp_platform/domain/quantity.py"],
        acceptance_checks=["py -m pytest tests/perp_platform/test_quantity.py -q"],
    )

    assert payload["model"] == "gpt-5.4"
    assert payload["reasoning_effort"] == "xhigh"
    assert payload["approval_bundle_id"] == "exec-2026-03-19-001"
    assert payload["issue_id"] == 29
