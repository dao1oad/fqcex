from __future__ import annotations

import pytest

from tests.perp_platform.support.config import import_perp_platform_module


def test_begin_binance_recovery_starts_backing_off_reduce_only() -> None:
    recovery_module = import_perp_platform_module("perp_platform.runtime.binance.recovery")

    state = recovery_module.begin_binance_recovery()

    assert state.phase == recovery_module.BinanceRecoveryPhase.BACKING_OFF
    assert state.trade_mode == "REDUCE_ONLY"
    assert state.attempt == 1
    assert state.backoff_seconds == 5
    assert state.subscriptions_restored is False
    assert state.reconciliation_required is False


def test_advance_binance_recovery_follows_expected_sequence() -> None:
    recovery_module = import_perp_platform_module("perp_platform.runtime.binance.recovery")

    backing_off = recovery_module.begin_binance_recovery()
    reconnecting = recovery_module.advance_binance_recovery(
        backing_off,
        recovery_module.BinanceRecoveryEvent.BACKOFF_ELAPSED,
    )
    private_restored = recovery_module.advance_binance_recovery(
        reconnecting,
        recovery_module.BinanceRecoveryEvent.PRIVATE_STREAM_READY,
    )
    reconciliation_pending = recovery_module.advance_binance_recovery(
        private_restored,
        recovery_module.BinanceRecoveryEvent.RESUBSCRIBE_COMPLETED,
    )

    assert reconnecting.phase == recovery_module.BinanceRecoveryPhase.RECONNECTING
    assert reconnecting.backoff_seconds == 5
    assert private_restored.phase == (
        recovery_module.BinanceRecoveryPhase.PRIVATE_STREAM_RESTORED
    )
    assert reconciliation_pending.phase == (
        recovery_module.BinanceRecoveryPhase.RECONCILIATION_PENDING
    )
    assert reconciliation_pending.subscriptions_restored is True
    assert reconciliation_pending.reconciliation_required is True


def test_rate_limit_hit_restarts_backoff_with_higher_attempt() -> None:
    recovery_module = import_perp_platform_module("perp_platform.runtime.binance.recovery")

    state = recovery_module.begin_binance_recovery()
    state = recovery_module.advance_binance_recovery(
        state,
        recovery_module.BinanceRecoveryEvent.BACKOFF_ELAPSED,
    )
    state = recovery_module.advance_binance_recovery(
        state,
        recovery_module.BinanceRecoveryEvent.RATE_LIMIT_HIT,
    )

    assert state.phase == recovery_module.BinanceRecoveryPhase.BACKING_OFF
    assert state.trade_mode == "REDUCE_ONLY"
    assert state.attempt == 2
    assert state.backoff_seconds == 10
    assert state.subscriptions_restored is False
    assert state.reconciliation_required is False


def test_backoff_seconds_is_capped_after_repeated_rate_limit_hits() -> None:
    recovery_module = import_perp_platform_module("perp_platform.runtime.binance.recovery")

    state = recovery_module.begin_binance_recovery()
    for _ in range(6):
        state = recovery_module.advance_binance_recovery(
            state,
            recovery_module.BinanceRecoveryEvent.BACKOFF_ELAPSED,
        )
        state = recovery_module.advance_binance_recovery(
            state,
            recovery_module.BinanceRecoveryEvent.RATE_LIMIT_HIT,
        )

    assert state.phase == recovery_module.BinanceRecoveryPhase.BACKING_OFF
    assert state.attempt == 7
    assert state.backoff_seconds == 60


def test_resubscribe_before_private_stream_ready_is_rejected() -> None:
    recovery_module = import_perp_platform_module("perp_platform.runtime.binance.recovery")

    state = recovery_module.begin_binance_recovery()
    state = recovery_module.advance_binance_recovery(
        state,
        recovery_module.BinanceRecoveryEvent.BACKOFF_ELAPSED,
    )

    with pytest.raises(ValueError):
        recovery_module.advance_binance_recovery(
            state,
            recovery_module.BinanceRecoveryEvent.RESUBSCRIBE_COMPLETED,
        )
