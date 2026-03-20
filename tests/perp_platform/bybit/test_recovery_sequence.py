from __future__ import annotations

import pytest

from tests.perp_platform.support.config import import_perp_platform_module


def test_begin_bybit_recovery_starts_reconnecting_reduce_only() -> None:
    recovery_module = import_perp_platform_module("perp_platform.runtime.bybit.recovery")

    state = recovery_module.begin_bybit_recovery()

    assert state.phase == recovery_module.BybitRecoveryPhase.RECONNECTING
    assert state.trade_mode == "REDUCE_ONLY"
    assert state.subscriptions_restored is False
    assert state.reconciliation_required is False


def test_advance_bybit_recovery_follows_expected_sequence() -> None:
    recovery_module = import_perp_platform_module("perp_platform.runtime.bybit.recovery")

    reconnecting = recovery_module.begin_bybit_recovery()
    private_restored = recovery_module.advance_bybit_recovery(
        reconnecting,
        recovery_module.BybitRecoveryEvent.PRIVATE_STREAM_READY,
    )
    reconciliation_pending = recovery_module.advance_bybit_recovery(
        private_restored,
        recovery_module.BybitRecoveryEvent.RESUBSCRIBE_COMPLETED,
    )

    assert private_restored.phase == recovery_module.BybitRecoveryPhase.PRIVATE_STREAM_RESTORED
    assert private_restored.trade_mode == "REDUCE_ONLY"
    assert private_restored.subscriptions_restored is False
    assert private_restored.reconciliation_required is False

    assert reconciliation_pending.phase == recovery_module.BybitRecoveryPhase.RECONCILIATION_PENDING
    assert reconciliation_pending.trade_mode == "REDUCE_ONLY"
    assert reconciliation_pending.subscriptions_restored is True
    assert reconciliation_pending.reconciliation_required is True


def test_advance_bybit_recovery_rejects_resubscribe_before_private_ready() -> None:
    recovery_module = import_perp_platform_module("perp_platform.runtime.bybit.recovery")

    state = recovery_module.begin_bybit_recovery()

    with pytest.raises(ValueError):
        recovery_module.advance_bybit_recovery(
            state,
            recovery_module.BybitRecoveryEvent.RESUBSCRIBE_COMPLETED,
        )


def test_advance_bybit_recovery_rejects_advancing_terminal_state() -> None:
    recovery_module = import_perp_platform_module("perp_platform.runtime.bybit.recovery")

    state = recovery_module.begin_bybit_recovery()
    state = recovery_module.advance_bybit_recovery(
        state,
        recovery_module.BybitRecoveryEvent.PRIVATE_STREAM_READY,
    )
    state = recovery_module.advance_bybit_recovery(
        state,
        recovery_module.BybitRecoveryEvent.RESUBSCRIBE_COMPLETED,
    )

    with pytest.raises(ValueError):
        recovery_module.advance_bybit_recovery(
            state,
            recovery_module.BybitRecoveryEvent.PRIVATE_STREAM_READY,
        )
