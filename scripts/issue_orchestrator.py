from __future__ import annotations

import argparse
from datetime import datetime
import json
from pathlib import Path

from perp_platform.orchestrator.dispatcher import build_owner_dispatch_payload
from perp_platform.orchestrator.models import ApprovalBundle
from perp_platform.orchestrator.github_state import (
    find_claimable_task_work_item,
    find_task_work_item,
    load_task_work_items,
)
from perp_platform.orchestrator.runtime_state import (
    load_approval_bundle,
    load_state,
    save_approval_bundle,
    save_state,
)
from perp_platform.orchestrator.sequence import select_next_ready_issue


DEFAULT_APPROVAL_PATH = Path(".codex/orchestrator/approval_bundle.json")


def slugify_issue_title(issue_title: str) -> str:
    return "-".join(issue_title.lower().split())


def build_default_approval_bundle(issue_start: int, issue_end: int) -> ApprovalBundle:
    return ApprovalBundle(
        bundle_id=f"exec-{datetime.now().strftime('%Y-%m-%d-%H%M%S')}",
        approved_by_user=True,
        approved_at=datetime.now().astimezone().isoformat(),
        scope_label=f"issues_{issue_start}_to_{issue_end}",
        issue_start=issue_start,
        issue_end=issue_end,
        execution_mode="proceed_with_recommended_defaults",
        issue_parallelism=1,
        write_agents_per_issue=1,
        read_only_sidecars_per_issue=2,
        merge_policy="auto_merge_main",
        close_policy="auto_close_child_and_update_tracking",
        reporting_policy="issue_completion_or_blocked_only",
        pause_only_on=(
            "sibling_issue_required",
            "adr_or_runbook_change_required",
            "phase_boundary_conflict",
            "forbidden_file_change",
            "repeated_nonconverging_failures",
        ),
        recommended_defaults=("recommended",),
        model="gpt-5.4",
        reasoning_effort="xhigh",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    status_parser = subparsers.add_parser("status")
    status_parser.add_argument("--state-path", default=".codex/orchestrator/state.json")

    next_parser = subparsers.add_parser("next")
    next_parser.add_argument("--issues-path", required=True)

    claim_parser = subparsers.add_parser("claim")
    claim_parser.add_argument("issue_id", type=int)
    claim_parser.add_argument("--issues-path", required=True)
    claim_parser.add_argument("--state-path", default=".codex/orchestrator/state.json")

    prepare_parser = subparsers.add_parser("prepare")
    prepare_parser.add_argument("issue_id", type=int)
    prepare_parser.add_argument("--issues-path", required=True)
    prepare_parser.add_argument("--approval-path", default=str(DEFAULT_APPROVAL_PATH))

    accept_parser = subparsers.add_parser("accept")
    accept_parser.add_argument("issue_id", type=int)
    accept_parser.add_argument("--state-path", default=".codex/orchestrator/state.json")
    accept_parser.add_argument("--head-sha", required=True)
    accept_parser.add_argument("--changed-files-path", required=True)
    accept_parser.add_argument("--review-evidence-path", required=True)

    block_parser = subparsers.add_parser("block")
    block_parser.add_argument("issue_id", type=int)
    block_parser.add_argument("--state-path", default=".codex/orchestrator/state.json")
    block_parser.add_argument("--reason", required=True)

    close_parser = subparsers.add_parser("close")
    close_parser.add_argument("issue_id", type=int)
    close_parser.add_argument("--state-path", default=".codex/orchestrator/state.json")

    approval_parser = subparsers.add_parser("approval")
    approval_subparsers = approval_parser.add_subparsers(dest="approval_command", required=True)

    approval_create_parser = approval_subparsers.add_parser("create")
    approval_create_parser.add_argument("--issue-start", type=int, required=True)
    approval_create_parser.add_argument("--issue-end", type=int, required=True)
    approval_create_parser.add_argument(
        "--approval-path", default=str(DEFAULT_APPROVAL_PATH)
    )

    approval_show_parser = approval_subparsers.add_parser("show")
    approval_show_parser.add_argument("--approval-path", default=str(DEFAULT_APPROVAL_PATH))

    approval_check_parser = approval_subparsers.add_parser("check")
    approval_check_parser.add_argument("--issue", type=int, required=True)
    approval_check_parser.add_argument("--approval-path", default=str(DEFAULT_APPROVAL_PATH))

    args = parser.parse_args()

    if args.command == "status":
        work_item = load_state(Path(args.state_path))
        print(f"{work_item.issue_id} {work_item.status}")
        return 0

    if args.command == "next":
        work_items, closed_issue_ids = load_task_work_items(Path(args.issues_path))
        selected = select_next_ready_issue(work_items, closed_issue_ids)

        if selected is None:
            print("no ready issue")
            return 1

        print(f"{selected.issue_id} {selected.issue_title}")
        return 0

    if args.command == "claim":
        work_item = find_claimable_task_work_item(Path(args.issues_path), args.issue_id)

        if work_item is None:
            print("issue not claimable")
            return 1

        claimed_work_item = type(work_item)(
            issue_id=work_item.issue_id,
            issue_title=work_item.issue_title,
            tracking_issue_id=work_item.tracking_issue_id,
            status=type(work_item.status).CLAIMED,
            owner_agent_id=work_item.owner_agent_id,
            approval_bundle_id=work_item.approval_bundle_id,
            base_sha=work_item.base_sha,
            head_sha=work_item.head_sha,
            allowed_files=work_item.allowed_files,
        )
        save_state(Path(args.state_path), claimed_work_item)
        print(f"claimed {claimed_work_item.issue_id}")
        return 0

    if args.command == "prepare":
        work_item = find_claimable_task_work_item(Path(args.issues_path), args.issue_id)

        if work_item is None:
            print("issue not claimable")
            return 1

        approval_bundle = load_approval_bundle(Path(args.approval_path))
        if not (approval_bundle.issue_start <= work_item.issue_id <= approval_bundle.issue_end):
            print("out of approved scope")
            return 1

        issue_slug = f"issue-{work_item.issue_id}-{slugify_issue_title(work_item.issue_title)}"
        branch = f"codex/{issue_slug}"
        worktree_path = str(Path.cwd() / ".worktrees" / issue_slug)
        owner_payload = build_owner_dispatch_payload(
            work_item=work_item,
            approval_bundle=approval_bundle,
            worktree_path=worktree_path,
            allowed_files=[],
            acceptance_checks=[],
        )
        print(
            json.dumps(
                {
                    "branch": branch,
                    "worktree_path": worktree_path,
                    "owner_payload": owner_payload,
                }
            )
        )
        return 0

    if args.command == "accept":
        work_item = load_state(Path(args.state_path))

        if work_item.issue_id != args.issue_id:
            print("issue mismatch")
            return 1

        if work_item.head_sha != args.head_sha:
            print("head sha mismatch")
            return 1

        changed_files = json.loads(
            Path(args.changed_files_path).read_text(encoding="utf-8")
        )
        if any(changed_file not in work_item.allowed_files for changed_file in changed_files):
            print("boundary violation")
            return 1

        review_evidence = Path(args.review_evidence_path).read_text(encoding="utf-8")
        if not review_evidence.strip():
            print("missing review evidence")
            return 1

        print("accepted")
        return 0

    if args.command == "block":
        work_item = load_state(Path(args.state_path))

        if work_item.issue_id != args.issue_id:
            print("issue mismatch")
            return 1

        blocked_work_item = type(work_item)(
            issue_id=work_item.issue_id,
            issue_title=work_item.issue_title,
            tracking_issue_id=work_item.tracking_issue_id,
            status=type(work_item.status).BLOCKED,
            owner_agent_id=work_item.owner_agent_id,
            approval_bundle_id=work_item.approval_bundle_id,
            base_sha=work_item.base_sha,
            head_sha=work_item.head_sha,
            allowed_files=work_item.allowed_files,
            blocker_reason=args.reason,
        )
        save_state(Path(args.state_path), blocked_work_item)
        print("blocked")
        return 0

    if args.command == "close":
        work_item = load_state(Path(args.state_path))

        if work_item.issue_id != args.issue_id:
            print("issue mismatch")
            return 1

        Path(args.state_path).unlink(missing_ok=True)
        print("closed")
        return 0

    if args.command == "approval":
        approval_path = Path(args.approval_path)

        if args.approval_command == "create":
            approval_bundle = build_default_approval_bundle(
                issue_start=args.issue_start,
                issue_end=args.issue_end,
            )
            save_approval_bundle(approval_path, approval_bundle)
            print(approval_bundle.bundle_id)
            return 0

        approval_bundle = load_approval_bundle(approval_path)

        if args.approval_command == "show":
            print(
                f"{approval_bundle.scope_label} "
                f"{approval_bundle.model} "
                f"{approval_bundle.reasoning_effort}"
            )
            return 0

        if args.approval_command == "check":
            if approval_bundle.issue_start <= args.issue <= approval_bundle.issue_end:
                print("allowed")
                return 0

            print("out of approved scope")
            return 1

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
