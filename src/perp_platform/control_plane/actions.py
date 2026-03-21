from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class ForceResumePreconditions:
    recovery_completed: bool
    reconciliation_passed: bool
    has_critical_diffs: bool


@dataclass(frozen=True)
class OperatorActionRequest:
    action_type: str
    target_scope: dict
    requested_by: str
    reason: str
    requested_at: str
    preconditions: ForceResumePreconditions | None = None


@dataclass(frozen=True)
class OperatorActionResult:
    action_type: str
    target_scope: dict
    requested_by: str
    requested_at: str
    audit_event_id: str


class OperatorActionAuditHook(Protocol):
    def record(self, request: OperatorActionRequest) -> str: ...


@dataclass
class InMemoryOperatorActionAuditHook:
    _next_id: int = 1

    def record(self, request: OperatorActionRequest) -> str:
        audit_event_id = f"audit-{self._next_id}"
        self._next_id += 1
        return audit_event_id
