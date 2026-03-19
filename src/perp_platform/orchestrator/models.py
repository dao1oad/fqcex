"""Domain models for the issue orchestrator."""

from dataclasses import dataclass
from enum import StrEnum


class OrchestratorState(StrEnum):
    READY = "ready"
    CLAIMED = "claimed"
    CONTEXT_GATHERING = "context_gathering"
    DESIGNING = "designing"
    PLAN_READY = "plan_ready"
    DISPATCHED = "dispatched"
    IMPLEMENTING = "implementing"
    VERIFYING = "verifying"
    REVIEW_FIXING = "review_fixing"
    ACCEPTED = "accepted"
    MERGED = "merged"
    CLOSED = "closed"
    BLOCKED = "blocked"


class AgentRole(StrEnum):
    OWNER = "owner"
    EXPLORER = "explorer"
    VERIFIER = "verifier"
    REVIEWER = "reviewer"


@dataclass(frozen=True)
class WorkItem:
    issue_id: int
    issue_title: str
    tracking_issue_id: int
    status: OrchestratorState = OrchestratorState.READY
    owner_agent_id: str | None = None
    approval_bundle_id: str | None = None
    base_sha: str | None = None
    head_sha: str | None = None
    allowed_files: tuple[str, ...] = ()
    blocker_reason: str | None = None


@dataclass(frozen=True)
class ApprovalBundle:
    bundle_id: str
    approved_by_user: bool
    approved_at: str
    scope_label: str
    issue_start: int
    issue_end: int
    execution_mode: str
    issue_parallelism: int
    write_agents_per_issue: int
    read_only_sidecars_per_issue: int
    merge_policy: str
    close_policy: str
    reporting_policy: str
    pause_only_on: tuple[str, ...]
    recommended_defaults: tuple[str, ...]
    model: str
    reasoning_effort: str


@dataclass(frozen=True)
class IssueSnapshot:
    issue_id: int
    issue_title: str
    tracking_issue_id: int
    epic_issue_id: int
    sequence_index: int
    state: str
    type_label: str
    phase_labels: tuple[str, ...]
    area_labels: tuple[str, ...]
    assignees: tuple[str, ...]
    body: str
