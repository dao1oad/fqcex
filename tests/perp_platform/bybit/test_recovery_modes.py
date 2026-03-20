from __future__ import annotations

from tests.perp_platform.support.config import import_perp_platform_module


def _advance_to_reconciliation_pending():
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

    return recovery_module, state


def test_recovery_not_finished_keeps_reduce_only() -> None:
    recovery_module = import_perp_platform_module("perp_platform.runtime.bybit.recovery")
    tradeability_module = import_perp_platform_module(
        "perp_platform.runtime.bybit.tradeability"
    )

    recovery_state = recovery_module.begin_bybit_recovery()

    projection = tradeability_module.project_bybit_tradeability(
        recovery_state=recovery_state,
        reconciliation_result=None,
    )

    assert projection.mode == tradeability_module.BybitTradeabilityMode.REDUCE_ONLY
    assert projection.reason == "recovery_in_progress"
    assert projection.blockers == []


def test_reconciliation_failed_escalates_to_blocked_with_evidence() -> None:
    recovery_module, recovery_state = _advance_to_reconciliation_pending()
    reconciliation_module = import_perp_platform_module(
        "perp_platform.runtime.bybit.reconciliation"
    )
    tradeability_module = import_perp_platform_module(
        "perp_platform.runtime.bybit.tradeability"
    )

    reconciliation_result = reconciliation_module.reconcile_bybit_state(
        expected_orders=[
            reconciliation_module.BybitOrderSnapshot(order_id="o-1", status="NEW"),
        ],
        actual_orders=[
            reconciliation_module.BybitOrderSnapshot(order_id="o-2", status="NEW"),
        ],
        expected_positions=[
            reconciliation_module.BybitPositionSnapshot(
                instrument_id="BTCUSDT",
                base_qty="1.00",
            ),
        ],
        actual_positions=[
            reconciliation_module.BybitPositionSnapshot(
                instrument_id="BTCUSDT",
                base_qty="0.50",
            ),
        ],
        expected_balances=[
            reconciliation_module.BybitBalanceSnapshot(asset="USDT", wallet_balance="100"),
        ],
        actual_balances=[
            reconciliation_module.BybitBalanceSnapshot(asset="USDC", wallet_balance="100"),
        ],
    )

    projection = tradeability_module.project_bybit_tradeability(
        recovery_state=recovery_state,
        reconciliation_result=reconciliation_result,
    )

    assert recovery_state.phase == recovery_module.BybitRecoveryPhase.RECONCILIATION_PENDING
    assert reconciliation_result.passed is False
    assert projection.mode == tradeability_module.BybitTradeabilityMode.BLOCKED
    assert projection.reason == "reconciliation_failed"
    assert projection.blockers == [
        "missing_order:o-1",
        "unexpected_order:o-2",
        "mismatch_position:BTCUSDT:expected=1.00:actual=0.50",
        "missing_balance:USDT",
        "unexpected_balance:USDC",
    ]


def test_reconciliation_passed_keeps_reduce_only_with_cooldown_pending() -> None:
    _, recovery_state = _advance_to_reconciliation_pending()
    reconciliation_module = import_perp_platform_module(
        "perp_platform.runtime.bybit.reconciliation"
    )
    tradeability_module = import_perp_platform_module(
        "perp_platform.runtime.bybit.tradeability"
    )

    reconciliation_result = reconciliation_module.reconcile_bybit_state(
        expected_orders=[
            reconciliation_module.BybitOrderSnapshot(order_id="o-1", status="NEW"),
        ],
        actual_orders=[
            reconciliation_module.BybitOrderSnapshot(order_id="o-1", status="NEW"),
        ],
        expected_positions=[
            reconciliation_module.BybitPositionSnapshot(
                instrument_id="BTCUSDT",
                base_qty="1.00",
            ),
        ],
        actual_positions=[
            reconciliation_module.BybitPositionSnapshot(
                instrument_id="BTCUSDT",
                base_qty="1.00",
            ),
        ],
        expected_balances=[
            reconciliation_module.BybitBalanceSnapshot(asset="USDT", wallet_balance="100"),
        ],
        actual_balances=[
            reconciliation_module.BybitBalanceSnapshot(asset="USDT", wallet_balance="100"),
        ],
    )

    projection = tradeability_module.project_bybit_tradeability(
        recovery_state=recovery_state,
        reconciliation_result=reconciliation_result,
    )

    assert reconciliation_result.passed is True
    assert projection.mode == tradeability_module.BybitTradeabilityMode.REDUCE_ONLY
    assert projection.reason == "cooldown_pending"
    assert projection.blockers == []
