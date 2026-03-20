from __future__ import annotations

from tests.perp_platform.support.config import import_perp_platform_module


def test_recovery_in_progress_keeps_reduce_only_across_phases() -> None:
    recovery_module = import_perp_platform_module("perp_platform.runtime.binance.recovery")

    state = recovery_module.begin_binance_recovery()
    assert state.trade_mode == "REDUCE_ONLY"

    state = recovery_module.advance_binance_recovery(
        state,
        recovery_module.BinanceRecoveryEvent.BACKOFF_ELAPSED,
    )
    assert state.phase == recovery_module.BinanceRecoveryPhase.RECONNECTING
    assert state.trade_mode == "REDUCE_ONLY"

    state = recovery_module.advance_binance_recovery(
        state,
        recovery_module.BinanceRecoveryEvent.PRIVATE_STREAM_READY,
    )
    assert state.phase == recovery_module.BinanceRecoveryPhase.PRIVATE_STREAM_RESTORED
    assert state.trade_mode == "REDUCE_ONLY"
    assert state.subscriptions_restored is False


def test_recovery_sequence_ends_with_reconciliation_required() -> None:
    recovery_module = import_perp_platform_module("perp_platform.runtime.binance.recovery")

    state = recovery_module.begin_binance_recovery()
    state = recovery_module.advance_binance_recovery(
        state,
        recovery_module.BinanceRecoveryEvent.BACKOFF_ELAPSED,
    )
    state = recovery_module.advance_binance_recovery(
        state,
        recovery_module.BinanceRecoveryEvent.PRIVATE_STREAM_READY,
    )
    state = recovery_module.advance_binance_recovery(
        state,
        recovery_module.BinanceRecoveryEvent.RESUBSCRIBE_COMPLETED,
    )

    assert state.phase == recovery_module.BinanceRecoveryPhase.RECONCILIATION_PENDING
    assert state.trade_mode == "REDUCE_ONLY"
    assert state.subscriptions_restored is True
    assert state.reconciliation_required is True


def test_rate_limit_hit_resets_recovery_progress_but_preserves_safety_mode() -> None:
    recovery_module = import_perp_platform_module("perp_platform.runtime.binance.recovery")

    state = recovery_module.begin_binance_recovery()
    state = recovery_module.advance_binance_recovery(
        state,
        recovery_module.BinanceRecoveryEvent.BACKOFF_ELAPSED,
    )
    state = recovery_module.advance_binance_recovery(
        state,
        recovery_module.BinanceRecoveryEvent.PRIVATE_STREAM_READY,
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
