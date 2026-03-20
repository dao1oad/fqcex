"""Supervisor state machine contract for Phase 1."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class SupervisorState(StrEnum):
    """Canonical supervisor states."""

    LIVE = "LIVE"
    DEGRADED = "DEGRADED"
    RESYNCING = "RESYNCING"
    REDUCE_ONLY = "REDUCE_ONLY"
    BLOCKED = "BLOCKED"


@dataclass(frozen=True, slots=True)
class SupervisorTransition:
    """Supervisor transition outcome."""

    previous_state: SupervisorState
    next_state: SupervisorState
    reason: str
    changed: bool


_ALLOWED_TARGETS: dict[SupervisorState, tuple[SupervisorState, ...]] = {
    SupervisorState.LIVE: (
        SupervisorState.DEGRADED,
        SupervisorState.RESYNCING,
        SupervisorState.REDUCE_ONLY,
        SupervisorState.BLOCKED,
    ),
    SupervisorState.DEGRADED: (
        SupervisorState.LIVE,
        SupervisorState.RESYNCING,
        SupervisorState.REDUCE_ONLY,
        SupervisorState.BLOCKED,
    ),
    SupervisorState.RESYNCING: (
        SupervisorState.LIVE,
        SupervisorState.REDUCE_ONLY,
        SupervisorState.BLOCKED,
    ),
    SupervisorState.REDUCE_ONLY: (
        SupervisorState.LIVE,
        SupervisorState.BLOCKED,
    ),
    SupervisorState.BLOCKED: (SupervisorState.REDUCE_ONLY,),
}


def allowed_supervisor_targets(state: SupervisorState) -> tuple[SupervisorState, ...]:
    """Return allowed target states for ``state``.

    Same-state no-op transitions are handled in ``transition_supervisor_state``
    and therefore not included in the returned tuple.
    """

    return _ALLOWED_TARGETS[state]


def transition_supervisor_state(
    current_state: SupervisorState,
    next_state: SupervisorState,
    reason: str,
) -> SupervisorTransition:
    """Validate and execute a supervisor state transition contract."""

    if next_state == current_state:
        return SupervisorTransition(
            previous_state=current_state,
            next_state=next_state,
            reason=reason,
            changed=False,
        )

    if next_state not in allowed_supervisor_targets(current_state):
        raise ValueError(
            f"invalid supervisor transition: {current_state} -> {next_state}"
        )

    return SupervisorTransition(
        previous_state=current_state,
        next_state=next_state,
        reason=reason,
        changed=True,
    )
