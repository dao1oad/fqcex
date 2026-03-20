from __future__ import annotations

from tests.perp_platform.support.config import import_perp_platform_module


def test_project_bybit_tradeability_recovery_in_progress_returns_reduce_only() -> None:
    recovery_module = import_perp_platform_module("perp_platform.runtime.bybit.recovery")
    tradeability_module = import_perp_platform_module(
        "perp_platform.runtime.bybit.tradeability"
    )

    recovery_state = recovery_module.BybitRecoveryState(
        phase=recovery_module.BybitRecoveryPhase.PRIVATE_STREAM_RESTORED,
        trade_mode="REDUCE_ONLY",
        subscriptions_restored=False,
        reconciliation_required=False,
    )

    projection = tradeability_module.project_bybit_tradeability(
        recovery_state=recovery_state,
        reconciliation_result=None,
    )

    assert projection.mode == tradeability_module.BybitTradeabilityMode.REDUCE_ONLY
    assert projection.reason == "recovery_in_progress"
    assert projection.blockers == []


def test_project_bybit_tradeability_reconciliation_pending_without_result_reduce_only() -> None:
    recovery_module = import_perp_platform_module("perp_platform.runtime.bybit.recovery")
    tradeability_module = import_perp_platform_module(
        "perp_platform.runtime.bybit.tradeability"
    )

    recovery_state = recovery_module.BybitRecoveryState(
        phase=recovery_module.BybitRecoveryPhase.RECONCILIATION_PENDING,
        trade_mode="REDUCE_ONLY",
        subscriptions_restored=True,
        reconciliation_required=True,
    )

    projection = tradeability_module.project_bybit_tradeability(
        recovery_state=recovery_state,
        reconciliation_result=None,
    )

    assert projection.mode == tradeability_module.BybitTradeabilityMode.REDUCE_ONLY
    assert projection.reason == "reconciliation_pending"
    assert projection.blockers == []


def test_project_bybit_tradeability_reconciliation_failed_returns_blocked() -> None:
    recovery_module = import_perp_platform_module("perp_platform.runtime.bybit.recovery")
    reconciliation_module = import_perp_platform_module(
        "perp_platform.runtime.bybit.reconciliation"
    )
    tradeability_module = import_perp_platform_module(
        "perp_platform.runtime.bybit.tradeability"
    )

    recovery_state = recovery_module.BybitRecoveryState(
        phase=recovery_module.BybitRecoveryPhase.RECONCILIATION_PENDING,
        trade_mode="REDUCE_ONLY",
        subscriptions_restored=True,
        reconciliation_required=True,
    )
    reconciliation_result = reconciliation_module.BybitReconciliationResult(
        orders_match=False,
        positions_match=False,
        balances_match=False,
        passed=False,
        order_diffs=["missing_order:o-1"],
        position_diffs=["mismatch_position:BTCUSDT:expected=1:actual=0"],
        balance_diffs=["unexpected_balance:USDC"],
    )

    projection = tradeability_module.project_bybit_tradeability(
        recovery_state=recovery_state,
        reconciliation_result=reconciliation_result,
    )

    assert projection.mode == tradeability_module.BybitTradeabilityMode.BLOCKED
    assert projection.reason == "reconciliation_failed"
    assert projection.blockers == [
        "missing_order:o-1",
        "mismatch_position:BTCUSDT:expected=1:actual=0",
        "unexpected_balance:USDC",
    ]


def test_project_bybit_tradeability_reconciliation_passed_returns_reduce_only() -> None:
    recovery_module = import_perp_platform_module("perp_platform.runtime.bybit.recovery")
    reconciliation_module = import_perp_platform_module(
        "perp_platform.runtime.bybit.reconciliation"
    )
    tradeability_module = import_perp_platform_module(
        "perp_platform.runtime.bybit.tradeability"
    )

    recovery_state = recovery_module.BybitRecoveryState(
        phase=recovery_module.BybitRecoveryPhase.RECONCILIATION_PENDING,
        trade_mode="REDUCE_ONLY",
        subscriptions_restored=True,
        reconciliation_required=True,
    )
    reconciliation_result = reconciliation_module.BybitReconciliationResult(
        orders_match=True,
        positions_match=True,
        balances_match=True,
        passed=True,
        order_diffs=[],
        position_diffs=[],
        balance_diffs=[],
    )

    projection = tradeability_module.project_bybit_tradeability(
        recovery_state=recovery_state,
        reconciliation_result=reconciliation_result,
    )

    assert projection.mode == tradeability_module.BybitTradeabilityMode.REDUCE_ONLY
    assert projection.reason == "cooldown_pending"
    assert projection.blockers == []
