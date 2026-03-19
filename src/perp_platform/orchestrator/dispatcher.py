"""Dispatch helpers for the issue orchestrator."""

from .models import ApprovalBundle, WorkItem


def build_owner_dispatch_payload(
    *,
    work_item: WorkItem,
    approval_bundle: ApprovalBundle,
    worktree_path: str,
    allowed_files: list[str],
    acceptance_checks: list[str],
) -> dict[str, object]:
    return {
        "issue_id": work_item.issue_id,
        "issue_title": work_item.issue_title,
        "worktree_path": worktree_path,
        "allowed_files": allowed_files,
        "acceptance_checks": acceptance_checks,
        "approved_design": True,
        "approval_owner": "master_agent",
        "approval_bundle_id": approval_bundle.bundle_id,
        "execution_mode": approval_bundle.execution_mode,
        "recommended_defaults": list(approval_bundle.recommended_defaults),
        "escalation_triggers": list(approval_bundle.pause_only_on),
        "merge_policy": approval_bundle.merge_policy,
        "close_policy": approval_bundle.close_policy,
        "reporting_policy": approval_bundle.reporting_policy,
        "model": approval_bundle.model,
        "reasoning_effort": approval_bundle.reasoning_effort,
    }
