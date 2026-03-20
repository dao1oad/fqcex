from __future__ import annotations

import inspect
from dataclasses import dataclass
from decimal import Decimal
from typing import Any, Callable

from cryptofeed import FeedHandler
from cryptofeed.defines import (
    BINANCE_FUTURES,
    BYBIT,
    OKX as OKX_ID,
    PERPETUAL,
    TICKER,
)
from cryptofeed.exchanges import BinanceFutures, Bybit, OKX
from cryptofeed.symbols import Symbols

from ..domain import Venue
from .config import CheckerConfig
from .models import CheckerTopOfBook


_PHASE1_CRYPTFEED_SYMBOLS = {
    Venue.BYBIT: {
        "BTC-USDT-PERP": "BTCUSDT",
        "ETH-USDT-PERP": "ETHUSDT",
    },
    Venue.BINANCE: {
        "BTC-USDT-PERP": "BTCUSDT",
        "ETH-USDT-PERP": "ETHUSDT",
    },
    Venue.OKX: {
        "BTC-USDT-PERP": "BTC-USDT-SWAP",
        "ETH-USDT-PERP": "ETH-USDT-SWAP",
    },
}

_CRYPTFEED_EXCHANGE_IDS = {
    Venue.BYBIT: BYBIT,
    Venue.BINANCE: BINANCE_FUTURES,
    Venue.OKX: OKX_ID,
}

_CRYPTFEED_EXCHANGES = {
    Venue.BYBIT: Bybit,
    Venue.BINANCE: BinanceFutures,
    Venue.OKX: OKX,
}

_SIZE_FIELDS = {
    Venue.BYBIT: ("bid1Size", "ask1Size"),
    Venue.BINANCE: ("B", "A"),
    Venue.OKX: ("bidSz", "askSz"),
}

_EXCHANGE_SYMBOL_FIELDS = {
    Venue.BYBIT: "symbol",
    Venue.BINANCE: "s",
    Venue.OKX: "instId",
}


@dataclass(frozen=True)
class CheckerExchangeFeed:
    venue: Venue
    exchange_id: str
    subscription_channel: str
    exchange_symbols: tuple[str, ...]
    feed: object


@dataclass(frozen=True)
class CheckerFeedRuntime:
    feed_handler: object
    feeds: tuple[CheckerExchangeFeed, ...]


def _normalize_event_timestamp(timestamp: Any) -> float | None:
    if timestamp is None:
        return None

    normalized = float(timestamp)
    if normalized > 10_000_000_000:
        normalized /= 1000.0
    return normalized


def _extract_raw_value(raw: Any, field_name: str, *, venue: Venue) -> Any:
    if not isinstance(raw, dict):
        raise ValueError(f"{venue.value} ticker raw payload must be a mapping")
    if field_name not in raw:
        raise ValueError(
            f"{venue.value} ticker raw payload is missing required {field_name} size field"
        )
    return raw[field_name]


def _extract_exchange_symbol(raw: Any, *, venue: Venue) -> str:
    field_name = _EXCHANGE_SYMBOL_FIELDS[venue]
    return str(_extract_raw_value(raw, field_name, venue=venue))


def _extract_sizes(raw: Any, *, venue: Venue) -> tuple[Decimal | int | str, Decimal | int | str]:
    bid_field, ask_field = _SIZE_FIELDS[venue]
    return (
        _extract_raw_value(raw, bid_field, venue=venue),
        _extract_raw_value(raw, ask_field, venue=venue),
    )


def prime_checker_symbol_mappings(instrument_ids: tuple[str, ...]) -> None:
    for venue, symbol_map in _PHASE1_CRYPTFEED_SYMBOLS.items():
        normalized_symbols: dict[str, str] = {}
        instrument_type: dict[str, str] = {}

        for instrument_id in instrument_ids:
            if instrument_id not in symbol_map:
                raise ValueError(
                    f"{venue.value} does not have a Phase 1 Cryptofeed symbol mapping for {instrument_id}"
                )
            normalized_symbols[instrument_id] = symbol_map[instrument_id]
            instrument_type[instrument_id] = PERPETUAL

        Symbols.set(
            _CRYPTFEED_EXCHANGE_IDS[venue],
            normalized_symbols,
            {"instrument_type": instrument_type},
        )


def normalize_checker_ticker(
    venue: Venue,
    ticker: Any,
    *,
    receipt_timestamp: float,
) -> CheckerTopOfBook:
    bid_size, ask_size = _extract_sizes(ticker.raw, venue=venue)
    exchange_symbol = _extract_exchange_symbol(ticker.raw, venue=venue)

    return CheckerTopOfBook(
        venue=venue,
        instrument_id=str(ticker.symbol),
        exchange_symbol=exchange_symbol,
        bid_price=ticker.bid,
        bid_size=bid_size,
        ask_price=ticker.ask,
        ask_size=ask_size,
        event_timestamp=_normalize_event_timestamp(ticker.timestamp),
        receipt_timestamp=receipt_timestamp,
    )


def _make_ticker_callback(
    venue: Venue,
    on_top_of_book: Callable[[CheckerTopOfBook], object],
):
    async def callback(ticker: Any, receipt_timestamp: float) -> None:
        normalized = normalize_checker_ticker(
            venue,
            ticker,
            receipt_timestamp=receipt_timestamp,
        )
        result = on_top_of_book(normalized)
        if inspect.isawaitable(result):
            await result

    return callback


def build_checker_exchange_feeds(
    checker_config: CheckerConfig,
    on_top_of_book: Callable[[CheckerTopOfBook], object],
) -> tuple[CheckerExchangeFeed, ...]:
    prime_checker_symbol_mappings(checker_config.instrument_ids)

    registrations: list[CheckerExchangeFeed] = []
    for venue in checker_config.venues:
        exchange_cls = _CRYPTFEED_EXCHANGES[venue]
        feed = exchange_cls(
            symbols=list(checker_config.instrument_ids),
            channels=[TICKER],
            callbacks={TICKER: _make_ticker_callback(venue, on_top_of_book)},
        )
        subscription_channel, exchange_symbols = next(iter(feed.subscription.items()))
        registrations.append(
            CheckerExchangeFeed(
                venue=venue,
                exchange_id=exchange_cls.id,
                subscription_channel=subscription_channel,
                exchange_symbols=tuple(exchange_symbols),
                feed=feed,
            )
        )

    return tuple(registrations)


def build_checker_feed_handler(
    checker_config: CheckerConfig,
    on_top_of_book: Callable[[CheckerTopOfBook], object],
    *,
    feed_handler_cls: type | None = None,
) -> CheckerFeedRuntime:
    registrations = build_checker_exchange_feeds(checker_config, on_top_of_book)
    handler_class = FeedHandler if feed_handler_cls is None else feed_handler_cls
    feed_handler = handler_class()

    for registration in registrations:
        feed_handler.add_feed(registration.feed)

    return CheckerFeedRuntime(
        feed_handler=feed_handler,
        feeds=registrations,
    )
