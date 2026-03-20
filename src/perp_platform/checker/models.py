from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, InvalidOperation

from ..domain import Venue


def _to_decimal(value: Decimal | int | str, *, field_name: str) -> Decimal:
    if isinstance(value, bool) or isinstance(value, float):
        raise TypeError(f"{field_name} must not be a float")

    if isinstance(value, Decimal):
        decimal_value = value
    elif isinstance(value, int):
        decimal_value = Decimal(value)
    elif isinstance(value, str):
        candidate = value.strip()
        if not candidate:
            raise ValueError(f"{field_name} must not be empty")
        try:
            decimal_value = Decimal(candidate)
        except InvalidOperation as exc:
            raise ValueError(f"{field_name} must be a valid decimal") from exc
    else:
        raise TypeError(f"{field_name} must be Decimal, int, or str")

    if decimal_value <= 0:
        raise ValueError(f"{field_name} must be greater than 0")

    return decimal_value


@dataclass(frozen=True)
class CheckerTopOfBook:
    venue: Venue
    instrument_id: str
    exchange_symbol: str
    bid_price: Decimal
    bid_size: Decimal
    ask_price: Decimal
    ask_size: Decimal
    event_timestamp: float | None
    receipt_timestamp: float

    def __post_init__(self) -> None:
        instrument_id = self.instrument_id.strip().upper()
        if not instrument_id.endswith("-USDT-PERP"):
            raise ValueError(
                "instrument_id must stay within the canonical *-USDT-PERP Phase 1 boundary"
            )

        exchange_symbol = self.exchange_symbol.strip().upper()
        if not exchange_symbol:
            raise ValueError("exchange_symbol must not be empty")

        if self.event_timestamp is not None and self.event_timestamp <= 0:
            raise ValueError("event_timestamp must be greater than 0 when present")
        if self.receipt_timestamp <= 0:
            raise ValueError("receipt_timestamp must be greater than 0")

        object.__setattr__(self, "instrument_id", instrument_id)
        object.__setattr__(self, "exchange_symbol", exchange_symbol)
        object.__setattr__(
            self,
            "bid_price",
            _to_decimal(self.bid_price, field_name="bid_price"),
        )
        object.__setattr__(
            self,
            "bid_size",
            _to_decimal(self.bid_size, field_name="bid_size"),
        )
        object.__setattr__(
            self,
            "ask_price",
            _to_decimal(self.ask_price, field_name="ask_price"),
        )
        object.__setattr__(
            self,
            "ask_size",
            _to_decimal(self.ask_size, field_name="ask_size"),
        )
