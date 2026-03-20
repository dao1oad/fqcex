from __future__ import annotations

from decimal import Decimal

import pytest

from tests.perp_platform.support.config import import_perp_platform_module


def test_okx_contracts_to_base_qty_uses_base_per_contract() -> None:
    conversion = import_perp_platform_module("perp_platform.runtime.okx.conversion")

    base_qty = conversion.okx_contracts_to_base_qty("3", base_per_contract="0.01")

    assert base_qty == Decimal("0.03")


def test_normalize_okx_contract_quantity_returns_normalized_quantity() -> None:
    conversion = import_perp_platform_module("perp_platform.runtime.okx.conversion")

    normalized = conversion.normalize_okx_contract_quantity(
        "5",
        base_per_contract="0.001",
    )

    assert normalized.base_qty == Decimal("0.005")
    assert normalized.exchange_qty == Decimal("5")
    assert normalized.exchange_qty_kind.value == "CONTRACTS"
    assert normalized.base_per_exchange_qty == Decimal("0.001")


def test_normalize_okx_contract_quantity_requires_positive_base_per_contract() -> None:
    conversion = import_perp_platform_module("perp_platform.runtime.okx.conversion")

    with pytest.raises(ValueError, match="base_per_exchange_qty"):
        conversion.normalize_okx_contract_quantity("2", base_per_contract="0")


def test_normalize_okx_contract_quantity_rejects_float_inputs() -> None:
    conversion = import_perp_platform_module("perp_platform.runtime.okx.conversion")

    with pytest.raises(TypeError, match="float"):
        conversion.normalize_okx_contract_quantity(1.0, base_per_contract="0.01")
