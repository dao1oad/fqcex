from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class BybitOrderSnapshot:
    order_id: str
    status: str


@dataclass(frozen=True)
class BybitPositionSnapshot:
    instrument_id: str
    base_qty: str


@dataclass(frozen=True)
class BybitBalanceSnapshot:
    asset: str
    wallet_balance: str


@dataclass(frozen=True)
class BybitReconciliationResult:
    orders_match: bool
    positions_match: bool
    balances_match: bool
    passed: bool
    order_diffs: list[str]
    position_diffs: list[str]
    balance_diffs: list[str]


def _diff_by_key(
    expected: dict[str, str],
    actual: dict[str, str],
    *,
    label: str,
) -> list[str]:
    diffs: list[str] = []
    expected_keys = set(expected)
    actual_keys = set(actual)

    for missing_key in sorted(expected_keys - actual_keys):
        diffs.append(f"missing_{label}:{missing_key}")

    for unexpected_key in sorted(actual_keys - expected_keys):
        diffs.append(f"unexpected_{label}:{unexpected_key}")

    for shared_key in sorted(expected_keys & actual_keys):
        expected_value = expected[shared_key]
        actual_value = actual[shared_key]
        if expected_value != actual_value:
            diffs.append(
                f"mismatch_{label}:{shared_key}:expected={expected_value}:actual={actual_value}"
            )

    return diffs


def reconcile_bybit_state(
    expected_orders: list[BybitOrderSnapshot],
    actual_orders: list[BybitOrderSnapshot],
    expected_positions: list[BybitPositionSnapshot],
    actual_positions: list[BybitPositionSnapshot],
    expected_balances: list[BybitBalanceSnapshot],
    actual_balances: list[BybitBalanceSnapshot],
) -> BybitReconciliationResult:
    expected_order_map = {order.order_id: order.status for order in expected_orders}
    actual_order_map = {order.order_id: order.status for order in actual_orders}

    expected_position_map = {
        position.instrument_id: position.base_qty for position in expected_positions
    }
    actual_position_map = {
        position.instrument_id: position.base_qty for position in actual_positions
    }

    expected_balance_map = {
        balance.asset: balance.wallet_balance for balance in expected_balances
    }
    actual_balance_map = {
        balance.asset: balance.wallet_balance for balance in actual_balances
    }

    order_diffs = _diff_by_key(expected_order_map, actual_order_map, label="order")
    position_diffs = _diff_by_key(
        expected_position_map,
        actual_position_map,
        label="position",
    )
    balance_diffs = _diff_by_key(expected_balance_map, actual_balance_map, label="balance")

    orders_match = not order_diffs
    positions_match = not position_diffs
    balances_match = not balance_diffs

    return BybitReconciliationResult(
        orders_match=orders_match,
        positions_match=positions_match,
        balances_match=balances_match,
        passed=orders_match and positions_match and balances_match,
        order_diffs=order_diffs,
        position_diffs=position_diffs,
        balance_diffs=balance_diffs,
    )
