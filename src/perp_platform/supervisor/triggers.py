"""Supervisor trigger evaluation contract for Phase 1."""

from __future__ import annotations

from dataclasses import dataclass

from .state_machine import (
    SupervisorState,
    SupervisorTransition,
    transition_supervisor_state,
)

PUBLIC_DEGRADED_LAG_SECONDS = 1.5
PUBLIC_RESYNC_LAG_SECONDS = 3.0
PRIVATE_REDUCE_ONLY_LAG_SECONDS = 10.0


@dataclass(frozen=True, slots=True)
class SupervisorTriggerInputs:
    """Inputs used to evaluate supervisor trigger transitions."""

    public_stream_lag_seconds: float
    private_stream_lag_seconds: float
    reconciliation_failed: bool
    repeated_recovery_failure: bool


def evaluate_supervisor_triggers(
    current_state: SupervisorState,
    inputs: SupervisorTriggerInputs,
) -> SupervisorTransition:
    """Evaluate supervisor triggers and return a validated transition."""

    if inputs.reconciliation_failed:
        return transition_supervisor_state(
            current_state,
            SupervisorState.BLOCKED,
            reason="reconciliation_failed",
        )

    if inputs.repeated_recovery_failure:
        return transition_supervisor_state(
            current_state,
            SupervisorState.BLOCKED,
            reason="repeated_recovery_failure",
        )

    if inputs.private_stream_lag_seconds >= PRIVATE_REDUCE_ONLY_LAG_SECONDS:
        return transition_supervisor_state(
            current_state,
            SupervisorState.REDUCE_ONLY,
            reason="private_stream_lagging",
        )

    if inputs.public_stream_lag_seconds >= PUBLIC_RESYNC_LAG_SECONDS:
        if current_state in (SupervisorState.REDUCE_ONLY, SupervisorState.BLOCKED):
            return transition_supervisor_state(
                current_state,
                current_state,
                reason="current_state_stricter_than_resyncing",
            )
        return transition_supervisor_state(
            current_state,
            SupervisorState.RESYNCING,
            reason="public_stream_resync_required",
        )

    if inputs.public_stream_lag_seconds >= PUBLIC_DEGRADED_LAG_SECONDS:
        if current_state in (
            SupervisorState.RESYNCING,
            SupervisorState.REDUCE_ONLY,
            SupervisorState.BLOCKED,
        ):
            return transition_supervisor_state(
                current_state,
                current_state,
                reason="current_state_stricter_than_degraded",
            )
        return transition_supervisor_state(
            current_state,
            SupervisorState.DEGRADED,
            reason="public_stream_degraded",
        )

    if current_state is SupervisorState.REDUCE_ONLY:
        return transition_supervisor_state(
            current_state,
            SupervisorState.REDUCE_ONLY,
            reason="cooldown_or_manual_clear_required",
        )

    if current_state is SupervisorState.BLOCKED:
        return transition_supervisor_state(
            current_state,
            SupervisorState.BLOCKED,
            reason="manual_unblock_required",
        )

    return transition_supervisor_state(
        current_state,
        SupervisorState.LIVE,
        reason="healthy_streams",
    )
