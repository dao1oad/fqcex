from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from ..domain import Venue


DEFAULT_CHECKER_VENUES = (Venue.BYBIT, Venue.BINANCE, Venue.OKX)
DEFAULT_CHECKER_INSTRUMENTS = ("BTC-USDT-PERP", "ETH-USDT-PERP")


@dataclass(frozen=True)
class CheckerConfig:
    service_name: str
    venues: tuple[Venue, ...]
    instrument_ids: tuple[str, ...]


def _parse_venues(raw: str) -> tuple[Venue, ...]:
    if not raw.strip():
        return DEFAULT_CHECKER_VENUES

    venues: list[Venue] = []
    for token in raw.split(","):
        candidate = token.strip().upper()
        if not candidate:
            continue
        try:
            venues.append(Venue(candidate))
        except ValueError as exc:
            raise ValueError(
                "CHECKER_VENUES must only include: BYBIT, BINANCE, OKX"
            ) from exc

    if not venues:
        raise ValueError("CHECKER_VENUES must not be empty")

    return tuple(venues)


def _parse_instruments(raw: str) -> tuple[str, ...]:
    if not raw.strip():
        return DEFAULT_CHECKER_INSTRUMENTS

    instruments: list[str] = []
    for token in raw.split(","):
        candidate = token.strip().upper()
        if not candidate:
            continue
        if not candidate.endswith("-USDT-PERP"):
            raise ValueError(
                "CHECKER_INSTRUMENTS must only include canonical *-USDT-PERP instruments"
            )
        instruments.append(candidate)

    if not instruments:
        raise ValueError("CHECKER_INSTRUMENTS must not be empty")

    return tuple(instruments)


def load_checker_config(environ: Mapping[str, str] | None = None) -> CheckerConfig:
    source = {} if environ is None else environ

    service_name = (
        source.get("CHECKER_SERVICE_NAME", "cryptofeed-checker").strip()
        or "cryptofeed-checker"
    )
    venues = _parse_venues(source.get("CHECKER_VENUES", ""))
    instrument_ids = _parse_instruments(source.get("CHECKER_INSTRUMENTS", ""))

    return CheckerConfig(
        service_name=service_name,
        venues=venues,
        instrument_ids=instrument_ids,
    )
