from __future__ import annotations

from tests.perp_platform.support.config import import_perp_platform_module


def test_reconcile_bybit_state_passes_when_all_snapshots_match() -> None:
    reconciliation_module = import_perp_platform_module(
        "perp_platform.runtime.bybit.reconciliation"
    )

    result = reconciliation_module.reconcile_bybit_state(
        expected_orders=[
            reconciliation_module.BybitOrderSnapshot(order_id="o-1", status="NEW"),
        ],
        actual_orders=[
            reconciliation_module.BybitOrderSnapshot(order_id="o-1", status="NEW"),
        ],
        expected_positions=[
            reconciliation_module.BybitPositionSnapshot(
                instrument_id="BTCUSDT", base_qty="0.10"
            ),
        ],
        actual_positions=[
            reconciliation_module.BybitPositionSnapshot(
                instrument_id="BTCUSDT", base_qty="0.10"
            ),
        ],
        expected_balances=[
            reconciliation_module.BybitBalanceSnapshot(asset="USDT", wallet_balance="100"),
        ],
        actual_balances=[
            reconciliation_module.BybitBalanceSnapshot(asset="USDT", wallet_balance="100"),
        ],
    )

    assert result.orders_match is True
    assert result.positions_match is True
    assert result.balances_match is True
    assert result.passed is True
    assert result.order_diffs == []
    assert result.position_diffs == []
    assert result.balance_diffs == []


def test_reconcile_bybit_state_is_order_independent() -> None:
    reconciliation_module = import_perp_platform_module(
        "perp_platform.runtime.bybit.reconciliation"
    )

    result = reconciliation_module.reconcile_bybit_state(
        expected_orders=[
            reconciliation_module.BybitOrderSnapshot(order_id="o-1", status="NEW"),
            reconciliation_module.BybitOrderSnapshot(order_id="o-2", status="FILLED"),
        ],
        actual_orders=[
            reconciliation_module.BybitOrderSnapshot(order_id="o-2", status="FILLED"),
            reconciliation_module.BybitOrderSnapshot(order_id="o-1", status="NEW"),
        ],
        expected_positions=[
            reconciliation_module.BybitPositionSnapshot(
                instrument_id="ETHUSDT", base_qty="1"
            ),
            reconciliation_module.BybitPositionSnapshot(
                instrument_id="BTCUSDT", base_qty="0.10"
            ),
        ],
        actual_positions=[
            reconciliation_module.BybitPositionSnapshot(
                instrument_id="BTCUSDT", base_qty="0.10"
            ),
            reconciliation_module.BybitPositionSnapshot(
                instrument_id="ETHUSDT", base_qty="1"
            ),
        ],
        expected_balances=[
            reconciliation_module.BybitBalanceSnapshot(asset="USDC", wallet_balance="20"),
            reconciliation_module.BybitBalanceSnapshot(asset="USDT", wallet_balance="100"),
        ],
        actual_balances=[
            reconciliation_module.BybitBalanceSnapshot(asset="USDT", wallet_balance="100"),
            reconciliation_module.BybitBalanceSnapshot(asset="USDC", wallet_balance="20"),
        ],
    )

    assert result.passed is True


def test_reconcile_bybit_state_detects_order_diffs() -> None:
    reconciliation_module = import_perp_platform_module(
        "perp_platform.runtime.bybit.reconciliation"
    )

    result = reconciliation_module.reconcile_bybit_state(
        expected_orders=[
            reconciliation_module.BybitOrderSnapshot(order_id="o-1", status="NEW"),
            reconciliation_module.BybitOrderSnapshot(order_id="o-2", status="FILLED"),
        ],
        actual_orders=[
            reconciliation_module.BybitOrderSnapshot(order_id="o-1", status="CANCELLED"),
            reconciliation_module.BybitOrderSnapshot(order_id="o-3", status="NEW"),
        ],
        expected_positions=[],
        actual_positions=[],
        expected_balances=[],
        actual_balances=[],
    )

    assert result.orders_match is False
    assert result.passed is False
    assert result.order_diffs == [
        "missing_order:o-2",
        "unexpected_order:o-3",
        "mismatch_order:o-1:expected=NEW:actual=CANCELLED",
    ]


def test_reconcile_bybit_state_detects_position_diffs() -> None:
    reconciliation_module = import_perp_platform_module(
        "perp_platform.runtime.bybit.reconciliation"
    )

    result = reconciliation_module.reconcile_bybit_state(
        expected_orders=[],
        actual_orders=[],
        expected_positions=[
            reconciliation_module.BybitPositionSnapshot(
                instrument_id="BTCUSDT", base_qty="0.10"
            ),
        ],
        actual_positions=[
            reconciliation_module.BybitPositionSnapshot(
                instrument_id="BTCUSDT", base_qty="0.20"
            ),
        ],
        expected_balances=[],
        actual_balances=[],
    )

    assert result.positions_match is False
    assert result.passed is False
    assert result.position_diffs == [
        "mismatch_position:BTCUSDT:expected=0.10:actual=0.20",
    ]


def test_reconcile_bybit_state_detects_balance_diffs() -> None:
    reconciliation_module = import_perp_platform_module(
        "perp_platform.runtime.bybit.reconciliation"
    )

    result = reconciliation_module.reconcile_bybit_state(
        expected_orders=[],
        actual_orders=[],
        expected_positions=[],
        actual_positions=[],
        expected_balances=[
            reconciliation_module.BybitBalanceSnapshot(asset="USDT", wallet_balance="100"),
        ],
        actual_balances=[
            reconciliation_module.BybitBalanceSnapshot(asset="USDC", wallet_balance="100"),
        ],
    )

    assert result.balances_match is False
    assert result.passed is False
    assert result.balance_diffs == [
        "missing_balance:USDT",
        "unexpected_balance:USDC",
    ]
