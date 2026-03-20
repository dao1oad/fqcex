from tests.perp_platform.support.config import import_perp_platform_module


def _state_machine_module():
    return import_perp_platform_module("perp_platform.supervisor.state_machine")


def test_supervisor_state_enum_values_stable() -> None:
    state_machine = _state_machine_module()

    assert state_machine.SupervisorState.LIVE.value == "LIVE"
    assert state_machine.SupervisorState.DEGRADED.value == "DEGRADED"
    assert state_machine.SupervisorState.RESYNCING.value == "RESYNCING"
    assert state_machine.SupervisorState.REDUCE_ONLY.value == "REDUCE_ONLY"
    assert state_machine.SupervisorState.BLOCKED.value == "BLOCKED"


def test_allowed_targets_match_contract() -> None:
    state_machine = _state_machine_module()

    assert state_machine.allowed_supervisor_targets(state_machine.SupervisorState.LIVE) == (
        state_machine.SupervisorState.DEGRADED,
        state_machine.SupervisorState.RESYNCING,
        state_machine.SupervisorState.REDUCE_ONLY,
        state_machine.SupervisorState.BLOCKED,
    )
    assert state_machine.allowed_supervisor_targets(state_machine.SupervisorState.DEGRADED) == (
        state_machine.SupervisorState.LIVE,
        state_machine.SupervisorState.RESYNCING,
        state_machine.SupervisorState.REDUCE_ONLY,
        state_machine.SupervisorState.BLOCKED,
    )
    assert state_machine.allowed_supervisor_targets(state_machine.SupervisorState.RESYNCING) == (
        state_machine.SupervisorState.LIVE,
        state_machine.SupervisorState.REDUCE_ONLY,
        state_machine.SupervisorState.BLOCKED,
    )
    assert state_machine.allowed_supervisor_targets(state_machine.SupervisorState.REDUCE_ONLY) == (
        state_machine.SupervisorState.LIVE,
        state_machine.SupervisorState.BLOCKED,
    )
    assert state_machine.allowed_supervisor_targets(state_machine.SupervisorState.BLOCKED) == (
        state_machine.SupervisorState.REDUCE_ONLY,
    )


def test_valid_transition_succeeds() -> None:
    state_machine = _state_machine_module()

    result = state_machine.transition_supervisor_state(
        state_machine.SupervisorState.LIVE,
        state_machine.SupervisorState.DEGRADED,
        reason="public_feed_lagging",
    )

    assert result.previous_state == state_machine.SupervisorState.LIVE
    assert result.next_state == state_machine.SupervisorState.DEGRADED
    assert result.reason == "public_feed_lagging"
    assert result.changed is True


def test_same_state_transition_is_noop() -> None:
    state_machine = _state_machine_module()

    result = state_machine.transition_supervisor_state(
        state_machine.SupervisorState.RESYNCING,
        state_machine.SupervisorState.RESYNCING,
        reason="still_resyncing",
    )

    assert result.previous_state == state_machine.SupervisorState.RESYNCING
    assert result.next_state == state_machine.SupervisorState.RESYNCING
    assert result.reason == "still_resyncing"
    assert result.changed is False


def test_invalid_transition_raises_value_error() -> None:
    state_machine = _state_machine_module()

    try:
        state_machine.transition_supervisor_state(
            state_machine.SupervisorState.BLOCKED,
            state_machine.SupervisorState.LIVE,
            reason="manual_override",
        )
    except ValueError as exc:
        assert "BLOCKED" in str(exc)
        assert "LIVE" in str(exc)
    else:
        raise AssertionError("expected ValueError for BLOCKED -> LIVE transition")
