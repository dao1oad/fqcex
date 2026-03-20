from tests.perp_platform.support.config import import_perp_platform_module


def _state_machine_module():
    return import_perp_platform_module("perp_platform.supervisor.state_machine")


def _triggers_module():
    return import_perp_platform_module("perp_platform.supervisor.triggers")


def _projection_module():
    return import_perp_platform_module("perp_platform.supervisor.projection")


def _domain_module():
    return import_perp_platform_module("perp_platform.domain.instruments")


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


def test_state_flow_live_to_blocked_through_trigger_chain_and_projection() -> None:
    triggers = _triggers_module()
    projection = _projection_module()
    domain = _domain_module()

    current_state = triggers.SupervisorState.LIVE

    degraded = triggers.evaluate_supervisor_triggers(
        current_state,
        _inputs(triggers, public_lag=triggers.PUBLIC_DEGRADED_LAG_SECONDS),
    )
    assert degraded.next_state == triggers.SupervisorState.DEGRADED
    assert degraded.reason == "public_stream_degraded"

    degraded_projection = projection.project_venue_tradeability(
        domain.Venue.BYBIT,
        degraded.next_state,
        degraded.reason,
    )
    assert degraded_projection.allow_open is True
    assert degraded_projection.allow_reduce is True

    resyncing = triggers.evaluate_supervisor_triggers(
        degraded.next_state,
        _inputs(triggers, public_lag=triggers.PUBLIC_RESYNC_LAG_SECONDS),
    )
    assert resyncing.next_state == triggers.SupervisorState.RESYNCING
    assert resyncing.reason == "public_stream_resync_required"

    resyncing_projection = projection.project_venue_tradeability(
        domain.Venue.BYBIT,
        resyncing.next_state,
        resyncing.reason,
    )
    assert resyncing_projection.allow_open is False
    assert resyncing_projection.allow_reduce is True

    reduce_only = triggers.evaluate_supervisor_triggers(
        resyncing.next_state,
        _inputs(
            triggers,
            private_lag=triggers.PRIVATE_REDUCE_ONLY_LAG_SECONDS,
            public_lag=triggers.PUBLIC_RESYNC_LAG_SECONDS,
        ),
    )
    assert reduce_only.next_state == triggers.SupervisorState.REDUCE_ONLY
    assert reduce_only.reason == "private_stream_lagging"

    blocked = triggers.evaluate_supervisor_triggers(
        reduce_only.next_state,
        _inputs(triggers, reconciliation_failed=True),
    )
    assert blocked.next_state == triggers.SupervisorState.BLOCKED
    assert blocked.reason == "reconciliation_failed"

    blocked_projection = projection.project_venue_tradeability(
        domain.Venue.BYBIT,
        blocked.next_state,
        blocked.reason,
    )
    assert blocked_projection.allow_open is False
    assert blocked_projection.allow_reduce is False


def test_blocked_stays_blocked_even_when_inputs_are_healthy() -> None:
    triggers = _triggers_module()

    result = triggers.evaluate_supervisor_triggers(
        triggers.SupervisorState.BLOCKED,
        _inputs(triggers),
    )

    assert result.next_state == triggers.SupervisorState.BLOCKED
    assert result.reason == "manual_unblock_required"
    assert result.changed is False


def test_degraded_returns_to_live_when_inputs_recover() -> None:
    triggers = _triggers_module()

    result = triggers.evaluate_supervisor_triggers(
        triggers.SupervisorState.DEGRADED,
        _inputs(triggers),
    )

    assert result.next_state == triggers.SupervisorState.LIVE
    assert result.reason == "healthy_streams"
    assert result.changed is True


def test_instrument_override_cannot_relax_stricter_venue_projection() -> None:
    projection = _projection_module()
    domain = _domain_module()

    venue_projection = projection.project_venue_tradeability(
        domain.Venue.OKX,
        projection.SupervisorState.REDUCE_ONLY,
        reason="private_stream_lagging",
    )

    instrument_projection = projection.project_instrument_tradeability(
        venue_projection,
        domain.make_perp_instrument_id("BTC"),
        instrument_state=projection.SupervisorState.DEGRADED,
        reason="instrument_nominal",
    )

    assert instrument_projection.effective_state == projection.SupervisorState.REDUCE_ONLY
    assert instrument_projection.allow_open is False
    assert instrument_projection.allow_reduce is True
    assert instrument_projection.reason == "instrument_nominal"


def test_state_machine_rejects_blocked_to_live_transition() -> None:
    state_machine = _state_machine_module()

    try:
        state_machine.transition_supervisor_state(
            state_machine.SupervisorState.BLOCKED,
            state_machine.SupervisorState.LIVE,
            reason="healthy_streams",
        )
    except ValueError as exc:
        assert "BLOCKED" in str(exc)
        assert "LIVE" in str(exc)
    else:
        raise AssertionError("expected ValueError for BLOCKED -> LIVE transition")
