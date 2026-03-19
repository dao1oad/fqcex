from __future__ import annotations

import pytest

from tests.perp_platform.support.config import import_perp_platform_module


def load_instruments_module():
    return import_perp_platform_module("perp_platform.domain.instruments")


def test_make_perp_instrument_id_uses_canonical_format() -> None:
    instruments = load_instruments_module()

    instrument_id = instruments.make_perp_instrument_id("BTC")

    assert str(instrument_id) == "BTC-USDT-PERP"


def test_venue_enum_covers_phase1_venues() -> None:
    instruments = load_instruments_module()

    assert [venue.value for venue in instruments.Venue] == [
        "BYBIT",
        "BINANCE",
        "OKX",
    ]


def test_instrument_kind_enum_only_contains_perp() -> None:
    instruments = load_instruments_module()

    assert [kind.value for kind in instruments.InstrumentKind] == ["PERP"]


def test_instrument_id_preserves_structured_fields() -> None:
    instruments = load_instruments_module()

    instrument_id = instruments.make_perp_instrument_id("ETH")

    assert instrument_id.base == "ETH"
    assert instrument_id.quote == "USDT"
    assert instrument_id.kind is instruments.InstrumentKind.PERP


def test_instrument_id_rejects_invalid_base_symbol() -> None:
    instruments = load_instruments_module()

    with pytest.raises(ValueError, match="base"):
        instruments.make_perp_instrument_id("btc")
