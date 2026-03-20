from __future__ import annotations

from decimal import Decimal

from ...domain import NormalizedQuantity, Venue, normalize_quantity


def normalize_okx_contract_quantity(
    exchange_qty: Decimal | int | str,
    *,
    base_per_contract: Decimal | int | str,
) -> NormalizedQuantity:
    return normalize_quantity(
        Venue.OKX,
        exchange_qty,
        base_per_exchange_qty=base_per_contract,
    )


def okx_contracts_to_base_qty(
    exchange_qty: Decimal | int | str,
    *,
    base_per_contract: Decimal | int | str,
) -> Decimal:
    return normalize_okx_contract_quantity(
        exchange_qty,
        base_per_contract=base_per_contract,
    ).base_qty
