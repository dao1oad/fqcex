"""Dispatch helpers for the issue orchestrator."""

from .models import ApprovalBundle, IssueSnapshot, WorkItem


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


def build_dispatch_pack(
    *,
    snapshot: IssueSnapshot,
    work_item: WorkItem,
    approval_bundle: ApprovalBundle,
    branch: str,
    worktree_path: str,
    allowed_files: list[str],
    forbidden_files: list[str],
    acceptance_checks: list[str],
) -> dict[str, object]:
    owner_payload = build_owner_dispatch_payload(
        work_item=work_item,
        approval_bundle=approval_bundle,
        worktree_path=worktree_path,
        allowed_files=allowed_files,
        acceptance_checks=acceptance_checks,
    )

    execution_context = {
        "issue_id": snapshot.issue_id,
        "issue_title": snapshot.issue_title,
        "tracking_issue_id": snapshot.tracking_issue_id,
        "epic_issue_id": snapshot.epic_issue_id,
        "approval_bundle_id": approval_bundle.bundle_id,
        "model": approval_bundle.model,
        "reasoning_effort": approval_bundle.reasoning_effort,
    }
    constraints = {
        "allowed_files": allowed_files,
        "forbidden_files": forbidden_files,
        "acceptance_checks": acceptance_checks,
        "escalation_triggers": list(approval_bundle.pause_only_on),
        "review_requirements": [
            "review evidence required",
            "verification required before merge",
        ],
    }
    subagent_prompt = "\n".join(
        [
            f"You are the owner subagent for issue #{snapshot.issue_id}.",
            "The design has already been approved by the user through the master agent.",
            "",
            "Execution policy:",
            f"- Use {approval_bundle.model} with {approval_bundle.reasoning_effort} reasoning.",
            "- Do not ask the user for design confirmation.",
            "- Execute the approved recommended defaults.",
            f"- Work only in: {worktree_path}",
            "- Edit only the allowed files listed below.",
            "- Escalate only if you hit an approved escalation trigger.",
            "",
            f"Issue: #{snapshot.issue_id} {snapshot.issue_title}",
            f"Tracking: #{snapshot.tracking_issue_id}",
            f"Epic: #{snapshot.epic_issue_id}",
        ]
    )

    claim_record = {
        "issue_id": snapshot.issue_id,
        "issue_title": snapshot.issue_title,
        "tracking_issue_id": snapshot.tracking_issue_id,
        "epic_issue_id": snapshot.epic_issue_id,
        "approval_bundle_id": approval_bundle.bundle_id,
        "branch": branch,
        "worktree_path": worktree_path,
        "allowed_files": allowed_files,
        "forbidden_files": forbidden_files,
        "acceptance_checks": acceptance_checks,
        "model": approval_bundle.model,
        "reasoning_effort": approval_bundle.reasoning_effort,
    }
    acceptance_payload = {
        "issue_id": snapshot.issue_id,
        "approval_bundle_id": approval_bundle.bundle_id,
        "allowed_files": allowed_files,
        "review_required": True,
    }

    return {
        "branch": branch,
        "worktree_path": worktree_path,
        "owner_payload": owner_payload,
        "execution_context": execution_context,
        "constraints": constraints,
        "claim_record": claim_record,
        "acceptance_payload": acceptance_payload,
        "subagent_prompt": subagent_prompt,
    }
