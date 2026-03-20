"""Supervisor state machine public API."""

from .state_machine import (
    SupervisorState,
    SupervisorTransition,
    allowed_supervisor_targets,
    transition_supervisor_state,
)
from .triggers import (
    PRIVATE_REDUCE_ONLY_LAG_SECONDS,
    PUBLIC_DEGRADED_LAG_SECONDS,
    PUBLIC_RESYNC_LAG_SECONDS,
    SupervisorTriggerInputs,
    evaluate_supervisor_triggers,
)

__all__ = [
    "SupervisorState",
    "SupervisorTransition",
    "allowed_supervisor_targets",
    "transition_supervisor_state",
    "PRIVATE_REDUCE_ONLY_LAG_SECONDS",
    "PUBLIC_DEGRADED_LAG_SECONDS",
    "PUBLIC_RESYNC_LAG_SECONDS",
    "SupervisorTriggerInputs",
    "evaluate_supervisor_triggers",
]
