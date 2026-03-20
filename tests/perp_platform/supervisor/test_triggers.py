from tests.perp_platform.support.config import import_perp_platform_module


def _triggers_module():
    return import_perp_platform_module("perp_platform.supervisor.triggers")


def _inputs(
    triggers,
    *,
    public_lag: float = 0.0,
    private_lag: float = 0.0,
    reconciliation_failed: bool = False,
    repeated_recovery_failure: bool = False,
):
    return triggers.SupervisorTriggerInputs(
        public_stream_lag_seconds=public_lag,
        private_stream_lag_seconds=private_lag,
        reconciliation_failed=reconciliation_failed,
        repeated_recovery_failure=repeated_recovery_failure,
    )


def test_reconciliation_failure_transitions_to_blocked() -> None:
    triggers = _triggers_module()

    result = triggers.evaluate_supervisor_triggers(
        triggers.SupervisorState.LIVE,
        _inputs(triggers, reconciliation_failed=True),
    )

    assert result.next_state == triggers.SupervisorState.BLOCKED
    assert result.reason == "reconciliation_failed"
    assert result.changed is True


def test_repeated_recovery_failure_transitions_to_blocked() -> None:
    triggers = _triggers_module()

    result = triggers.evaluate_supervisor_triggers(
        triggers.SupervisorState.DEGRADED,
        _inputs(triggers, repeated_recovery_failure=True),
    )

    assert result.next_state == triggers.SupervisorState.BLOCKED
    assert result.reason == "repeated_recovery_failure"
    assert result.changed is True


def test_private_stale_transitions_to_reduce_only() -> None:
    triggers = _triggers_module()

    result = triggers.evaluate_supervisor_triggers(
        triggers.SupervisorState.LIVE,
        _inputs(
            triggers,
            private_lag=triggers.PRIVATE_REDUCE_ONLY_LAG_SECONDS,
        ),
    )

    assert result.next_state == triggers.SupervisorState.REDUCE_ONLY
    assert result.reason == "private_stream_lagging"
    assert result.changed is True


def test_public_lag_resync_threshold_transitions_to_resyncing() -> None:
    triggers = _triggers_module()

    result = triggers.evaluate_supervisor_triggers(
        triggers.SupervisorState.LIVE,
        _inputs(
            triggers,
            public_lag=triggers.PUBLIC_RESYNC_LAG_SECONDS,
        ),
    )

    assert result.next_state == triggers.SupervisorState.RESYNCING
    assert result.reason == "public_stream_resync_required"
    assert result.changed is True


def test_public_lag_degraded_threshold_transitions_to_degraded() -> None:
    triggers = _triggers_module()

    result = triggers.evaluate_supervisor_triggers(
        triggers.SupervisorState.LIVE,
        _inputs(
            triggers,
            public_lag=triggers.PUBLIC_DEGRADED_LAG_SECONDS,
        ),
    )

    assert result.next_state == triggers.SupervisorState.DEGRADED
    assert result.reason == "public_stream_degraded"
    assert result.changed is True


def test_healthy_inputs_transition_degraded_to_live() -> None:
    triggers = _triggers_module()

    result = triggers.evaluate_supervisor_triggers(
        triggers.SupervisorState.DEGRADED,
        _inputs(triggers),
    )

    assert result.next_state == triggers.SupervisorState.LIVE
    assert result.reason == "healthy_streams"
    assert result.changed is True


def test_healthy_inputs_keep_reduce_only_with_manual_clear_reason() -> None:
    triggers = _triggers_module()

    result = triggers.evaluate_supervisor_triggers(
        triggers.SupervisorState.REDUCE_ONLY,
        _inputs(triggers),
    )

    assert result.next_state == triggers.SupervisorState.REDUCE_ONLY
    assert result.reason == "cooldown_or_manual_clear_required"
    assert result.changed is False


def test_healthy_inputs_keep_blocked_with_manual_unblock_reason() -> None:
    triggers = _triggers_module()

    result = triggers.evaluate_supervisor_triggers(
        triggers.SupervisorState.BLOCKED,
        _inputs(triggers),
    )

    assert result.next_state == triggers.SupervisorState.BLOCKED
    assert result.reason == "manual_unblock_required"
    assert result.changed is False
