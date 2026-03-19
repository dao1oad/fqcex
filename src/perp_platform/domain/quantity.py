from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from enum import StrEnum

from .instruments import Venue


def _to_decimal(value: Decimal | int | str, *, field_name: str) -> Decimal:
    if isinstance(value, bool) or isinstance(value, float):
        raise TypeError(f"{field_name} must not be a float")

    if isinstance(value, Decimal):
        decimal_value = value
    elif isinstance(value, int):
        decimal_value = Decimal(value)
    elif isinstance(value, str):
        decimal_value = Decimal(value.strip())
    else:
        raise TypeError(f"{field_name} must be Decimal, int, or str")

    if decimal_value <= 0:
        raise ValueError(f"{field_name} must be greater than 0")

    return decimal_value


class ExchangeQtyKind(StrEnum):
    BASE = "BASE"
    CONTRACTS = "CONTRACTS"


@dataclass(frozen=True)
class NormalizedQuantity:
    base_qty: Decimal
    exchange_qty: Decimal
    exchange_qty_kind: ExchangeQtyKind
    base_per_exchange_qty: Decimal | None


def okx_contracts_to_base_qty(
    exchange_qty: Decimal | int | str,
    base_per_exchange_qty: Decimal | int | str,
) -> Decimal:
    contracts = _to_decimal(exchange_qty, field_name="exchange_qty")
    multiplier = _to_decimal(
        base_per_exchange_qty,
        field_name="base_per_exchange_qty",
    )
    return contracts * multiplier


def normalize_quantity(
    venue: Venue,
    exchange_qty: Decimal | int | str,
    *,
    base_per_exchange_qty: Decimal | int | str | None = None,
) -> NormalizedQuantity:
    normalized_exchange_qty = _to_decimal(exchange_qty, field_name="exchange_qty")
    venue_value = str(venue)

    if venue_value in {Venue.BYBIT.value, Venue.BINANCE.value}:
        if base_per_exchange_qty is not None:
            raise ValueError(
                "base_per_exchange_qty is only supported for OKX contract quantities"
            )

        return NormalizedQuantity(
            base_qty=normalized_exchange_qty,
            exchange_qty=normalized_exchange_qty,
            exchange_qty_kind=ExchangeQtyKind.BASE,
            base_per_exchange_qty=None,
        )

    if venue_value == Venue.OKX.value:
        if base_per_exchange_qty is None:
            raise ValueError("base_per_exchange_qty is required for OKX quantities")

        normalized_multiplier = _to_decimal(
            base_per_exchange_qty,
            field_name="base_per_exchange_qty",
        )
        return NormalizedQuantity(
            base_qty=normalized_exchange_qty * normalized_multiplier,
            exchange_qty=normalized_exchange_qty,
            exchange_qty_kind=ExchangeQtyKind.CONTRACTS,
            base_per_exchange_qty=normalized_multiplier,
        )

    raise ValueError(f"unsupported venue for quantity normalization: {venue}")
