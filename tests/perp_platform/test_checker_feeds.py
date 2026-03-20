from __future__ import annotations

from decimal import Decimal
from types import SimpleNamespace

import pytest

from tests.perp_platform.support.config import import_perp_platform_module


def _load_checker_config():
    config_module = import_perp_platform_module("perp_platform.checker.config")
    return config_module.load_checker_config({})


def test_build_checker_exchange_feeds_uses_phase1_symbol_mappings() -> None:
    feeds_module = import_perp_platform_module("perp_platform.checker.feeds")

    registrations = feeds_module.build_checker_exchange_feeds(
        _load_checker_config(),
        lambda update: None,
    )

    assert [
        (
            registration.venue.value,
            registration.exchange_id,
            registration.subscription_channel,
            registration.exchange_symbols,
        )
        for registration in registrations
    ] == [
        ("BYBIT", "BYBIT", "tickers", ("BTCUSDT", "ETHUSDT")),
        ("BINANCE", "BINANCE_FUTURES", "bookTicker", ("BTCUSDT", "ETHUSDT")),
        ("OKX", "OKX", "tickers", ("BTC-USDT-SWAP", "ETH-USDT-SWAP")),
    ]


def test_build_checker_feed_handler_adds_all_exchange_feeds() -> None:
    feeds_module = import_perp_platform_module("perp_platform.checker.feeds")

    class RecordingFeedHandler:
        def __init__(self) -> None:
            self.feeds: list[object] = []

        def add_feed(self, feed: object) -> None:
            self.feeds.append(feed)

    runtime = feeds_module.build_checker_feed_handler(
        _load_checker_config(),
        lambda update: None,
        feed_handler_cls=RecordingFeedHandler,
    )

    assert len(runtime.feeds) == 3
    assert len(runtime.feed_handler.feeds) == 3


@pytest.mark.parametrize(
    ("venue_name", "raw", "exchange_symbol", "bid_size", "ask_size"),
    [
        (
            "BYBIT",
            {
                "symbol": "BTCUSDT",
                "bid1Price": "65000.0",
                "bid1Size": "1.25",
                "ask1Price": "65000.5",
                "ask1Size": "1.50",
            },
            "BTCUSDT",
            "1.25",
            "1.50",
        ),
        (
            "BINANCE",
            {
                "s": "BTCUSDT",
                "b": "65000.0",
                "B": "2.00",
                "a": "65000.5",
                "A": "2.50",
            },
            "BTCUSDT",
            "2.00",
            "2.50",
        ),
        (
            "OKX",
            {
                "instId": "BTC-USDT-SWAP",
                "bidPx": "65000.0",
                "bidSz": "3.00",
                "askPx": "65000.5",
                "askSz": "3.50",
            },
            "BTC-USDT-SWAP",
            "3.00",
            "3.50",
        ),
    ],
)
def test_normalize_checker_ticker_returns_unified_top_of_book(
    venue_name: str,
    raw: dict[str, str],
    exchange_symbol: str,
    bid_size: str,
    ask_size: str,
) -> None:
    feeds_module = import_perp_platform_module("perp_platform.checker.feeds")
    instruments_module = import_perp_platform_module("perp_platform.domain.instruments")

    ticker = SimpleNamespace(
        symbol="BTC-USDT-PERP",
        bid=Decimal("65000.0"),
        ask=Decimal("65000.5"),
        timestamp=1711111111.0,
        raw=raw,
    )

    normalized = feeds_module.normalize_checker_ticker(
        instruments_module.Venue[venue_name],
        ticker,
        receipt_timestamp=1711111111.5,
    )

    assert normalized.venue == instruments_module.Venue[venue_name]
    assert normalized.instrument_id == "BTC-USDT-PERP"
    assert normalized.exchange_symbol == exchange_symbol
    assert normalized.bid_price == Decimal("65000.0")
    assert normalized.bid_size == Decimal(bid_size)
    assert normalized.ask_price == Decimal("65000.5")
    assert normalized.ask_size == Decimal(ask_size)
    assert normalized.event_timestamp == 1711111111.0
    assert normalized.receipt_timestamp == 1711111111.5


def test_normalize_checker_ticker_rejects_missing_size_fields() -> None:
    feeds_module = import_perp_platform_module("perp_platform.checker.feeds")
    instruments_module = import_perp_platform_module("perp_platform.domain.instruments")

    ticker = SimpleNamespace(
        symbol="BTC-USDT-PERP",
        bid=Decimal("65000.0"),
        ask=Decimal("65000.5"),
        timestamp=1711111111.0,
        raw={"s": "BTCUSDT", "b": "65000.0", "a": "65000.5"},
    )

    with pytest.raises(ValueError, match="size"):
        feeds_module.normalize_checker_ticker(
            instruments_module.Venue.BINANCE,
            ticker,
            receipt_timestamp=1711111111.5,
        )
