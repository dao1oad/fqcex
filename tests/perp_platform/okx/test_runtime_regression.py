from __future__ import annotations

from decimal import Decimal

import pytest

from tests.perp_platform.support.config import import_perp_platform_module


def _bootstrap_result():
    okx = import_perp_platform_module("perp_platform.runtime.okx")
    return okx, okx.bootstrap_okx_runtime(
        {
            "PERP_PLATFORM_APP_NAME": "perp-platform",
            "PERP_PLATFORM_ENVIRONMENT": "test",
            "PERP_PLATFORM_LOG_LEVEL": "INFO",
            "OKX_ENVIRONMENT": "demo",
            "OKX_API_KEY": "key-123",
            "OKX_API_SECRET": "secret-456",
            "OKX_API_PASSPHRASE": "pass-789",
        }
    )


def test_okx_package_conversion_and_runtime_projection_stay_consistent() -> None:
    okx, result = _bootstrap_result()

    normalized = okx.normalize_okx_contract_quantity("12", base_per_contract="0.001")

    assert okx.okx_contracts_to_base_qty("12", base_per_contract="0.001") == Decimal("0.012")
    assert normalized.base_qty == Decimal("0.012")
    assert normalized.exchange_qty == Decimal("12")
    assert normalized.exchange_qty_kind.value == "CONTRACTS"
    assert result.runtime.instrument_type == "SWAP"
    assert result.runtime.settle_asset == "USDT"
    assert result.runtime.position_mode == result.guards.position_mode == "net"
    assert result.runtime.margin_mode == result.guards.margin_mode == "isolated"


@pytest.mark.parametrize(
    ("order_type", "time_in_force", "reduce_only"),
    [("LIMIT", "GTC", False), ("MARKET", "IOC", True)],
)
def test_okx_package_guards_accept_phase1_supported_order_modes(
    order_type: str,
    time_in_force: str,
    reduce_only: bool,
) -> None:
    okx, result = _bootstrap_result()

    okx.validate_okx_order_capability(
        order_type=order_type,
        time_in_force=time_in_force,
        reduce_only=reduce_only,
        guards=result.guards,
    )


def test_okx_package_guards_reject_market_gtc_regression() -> None:
    okx, result = _bootstrap_result()

    with pytest.raises(ValueError, match="MARKET"):
        okx.validate_okx_order_capability(
            order_type="MARKET",
            time_in_force="GTC",
            reduce_only=False,
            guards=result.guards,
        )
