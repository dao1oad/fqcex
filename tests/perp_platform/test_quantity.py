from __future__ import annotations

from decimal import Decimal

import pytest

from tests.perp_platform.support.config import import_perp_platform_module


def load_domain_modules():
    instruments = import_perp_platform_module("perp_platform.domain.instruments")
    quantity = import_perp_platform_module("perp_platform.domain.quantity")
    return instruments, quantity


def test_bybit_quantity_normalizes_to_base_qty() -> None:
    instruments, quantity = load_domain_modules()

    normalized = quantity.normalize_quantity(instruments.Venue.BYBIT, "1.5")

    assert normalized.base_qty == Decimal("1.5")
    assert normalized.exchange_qty == Decimal("1.5")
    assert normalized.exchange_qty_kind is quantity.ExchangeQtyKind.BASE
    assert normalized.base_per_exchange_qty is None


def test_binance_quantity_normalizes_to_base_qty() -> None:
    instruments, quantity = load_domain_modules()

    normalized = quantity.normalize_quantity(instruments.Venue.BINANCE, Decimal("2"))

    assert normalized.base_qty == Decimal("2")
    assert normalized.exchange_qty == Decimal("2")
    assert normalized.exchange_qty_kind is quantity.ExchangeQtyKind.BASE


def test_okx_contracts_use_base_per_exchange_qty() -> None:
    instruments, quantity = load_domain_modules()

    normalized = quantity.normalize_quantity(
        instruments.Venue.OKX,
        "3",
        base_per_exchange_qty="0.01",
    )

    assert normalized.base_qty == Decimal("0.03")
    assert normalized.exchange_qty == Decimal("3")
    assert normalized.exchange_qty_kind is quantity.ExchangeQtyKind.CONTRACTS
    assert normalized.base_per_exchange_qty == Decimal("0.01")


def test_okx_requires_base_per_exchange_qty() -> None:
    instruments, quantity = load_domain_modules()

    with pytest.raises(ValueError, match="base_per_exchange_qty"):
        quantity.normalize_quantity(instruments.Venue.OKX, "3")


def test_normalize_quantity_rejects_non_positive_values() -> None:
    instruments, quantity = load_domain_modules()

    with pytest.raises(ValueError, match="exchange_qty"):
        quantity.normalize_quantity(instruments.Venue.BYBIT, "0")


def test_normalize_quantity_rejects_float_inputs() -> None:
    instruments, quantity = load_domain_modules()

    with pytest.raises(TypeError, match="float"):
        quantity.normalize_quantity(instruments.Venue.OKX, 1.0, base_per_exchange_qty="0.01")
