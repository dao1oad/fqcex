from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


def _validate_symbol_part(name: str, value: str) -> str:
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{name} must be a non-empty uppercase symbol")

    if normalized != normalized.upper() or not normalized.isascii():
        raise ValueError(f"{name} must be a non-empty uppercase symbol")

    if not all(character.isalnum() for character in normalized):
        raise ValueError(f"{name} must contain only uppercase letters or digits")

    return normalized


class Venue(StrEnum):
    BYBIT = "BYBIT"
    BINANCE = "BINANCE"
    OKX = "OKX"


class InstrumentKind(StrEnum):
    PERP = "PERP"


@dataclass(frozen=True)
class InstrumentId:
    base: str
    quote: str
    kind: InstrumentKind

    def __post_init__(self) -> None:
        object.__setattr__(self, "base", _validate_symbol_part("base", self.base))
        object.__setattr__(self, "quote", _validate_symbol_part("quote", self.quote))

    def __str__(self) -> str:
        return f"{self.base}-{self.quote}-{self.kind}"


def make_perp_instrument_id(base: str, quote: str = "USDT") -> InstrumentId:
    return InstrumentId(
        base=base,
        quote=quote,
        kind=InstrumentKind.PERP,
    )
