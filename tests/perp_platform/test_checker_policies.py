from __future__ import annotations

from decimal import Decimal

import pytest

from tests.perp_platform.support.config import import_perp_platform_module


def _checker_top_of_book(*, receipt_timestamp: float = 100.0):
    checker_models = import_perp_platform_module("perp_platform.checker.models")
    instruments_module = import_perp_platform_module("perp_platform.domain.instruments")

    return checker_models.CheckerTopOfBook(
        venue=instruments_module.Venue.BYBIT,
        instrument_id="BTC-USDT-PERP",
        exchange_symbol="BTCUSDT",
        bid_price=Decimal("65000.0"),
        bid_size=Decimal("1.25"),
        ask_price=Decimal("65000.5"),
        ask_size=Decimal("1.50"),
        event_timestamp=receipt_timestamp - 0.1,
        receipt_timestamp=receipt_timestamp,
    )


def _reference_top_of_book(*, bid_price: str = "65000.0", ask_price: str = "65000.5"):
    policies_module = import_perp_platform_module("perp_platform.checker.policies")
    instruments_module = import_perp_platform_module("perp_platform.domain.instruments")

    return policies_module.CheckerReferenceTopOfBook(
        venue=instruments_module.Venue.BYBIT,
        instrument_id="BTC-USDT-PERP",
        bid_price=Decimal(bid_price),
        ask_price=Decimal(ask_price),
        observed_timestamp=100.0,
    )


def test_evaluate_checker_policies_returns_healthy_result_within_thresholds() -> None:
    policies_module = import_perp_platform_module("perp_platform.checker.policies")

    result = policies_module.evaluate_checker_policies(
        _checker_top_of_book(receipt_timestamp=100.0),
        _reference_top_of_book(),
        now_timestamp=101.0,
        thresholds=policies_module.CheckerPolicyThresholds(
            max_staleness_seconds=3.0,
            max_divergence_bps=Decimal("5.0"),
        ),
    )

    assert result.age_seconds == 1.0
    assert result.stale is False
    assert result.bid_divergence_bps == Decimal("0")
    assert result.ask_divergence_bps == Decimal("0")
    assert result.max_divergence_bps == Decimal("0")
    assert result.diverged is False


def test_evaluate_checker_policies_marks_stale_when_receipt_lag_exceeds_threshold() -> None:
    policies_module = import_perp_platform_module("perp_platform.checker.policies")

    result = policies_module.evaluate_checker_policies(
        _checker_top_of_book(receipt_timestamp=100.0),
        _reference_top_of_book(),
        now_timestamp=103.5,
        thresholds=policies_module.CheckerPolicyThresholds(
            max_staleness_seconds=3.0,
            max_divergence_bps=Decimal("5.0"),
        ),
    )

    assert result.age_seconds == 3.5
    assert result.stale is True
    assert result.diverged is False


@pytest.mark.parametrize(
    ("reference_bid", "reference_ask", "expected_max_bps"),
    [
        ("64950.0", "65000.5", Decimal("7.698229407236335642802155504")),
        ("65000.0", "65050.5", Decimal("7.686336000491925504031483232")),
    ],
)
def test_evaluate_checker_policies_marks_diverged_when_bid_or_ask_exceeds_threshold(
    reference_bid: str,
    reference_ask: str,
    expected_max_bps: Decimal,
) -> None:
    policies_module = import_perp_platform_module("perp_platform.checker.policies")

    result = policies_module.evaluate_checker_policies(
        _checker_top_of_book(receipt_timestamp=100.0),
        _reference_top_of_book(
            bid_price=reference_bid,
            ask_price=reference_ask,
        ),
        now_timestamp=101.0,
        thresholds=policies_module.CheckerPolicyThresholds(
            max_staleness_seconds=3.0,
            max_divergence_bps=Decimal("5.0"),
        ),
    )

    assert result.stale is False
    assert result.diverged is True
    assert result.max_divergence_bps == expected_max_bps


def test_evaluate_checker_policies_rejects_mismatched_identity() -> None:
    checker_models = import_perp_platform_module("perp_platform.checker.models")
    policies_module = import_perp_platform_module("perp_platform.checker.policies")
    instruments_module = import_perp_platform_module("perp_platform.domain.instruments")

    checker_book = checker_models.CheckerTopOfBook(
        venue=instruments_module.Venue.BYBIT,
        instrument_id="BTC-USDT-PERP",
        exchange_symbol="BTCUSDT",
        bid_price=Decimal("65000.0"),
        bid_size=Decimal("1.25"),
        ask_price=Decimal("65000.5"),
        ask_size=Decimal("1.50"),
        event_timestamp=99.9,
        receipt_timestamp=100.0,
    )
    reference_book = policies_module.CheckerReferenceTopOfBook(
        venue=instruments_module.Venue.OKX,
        instrument_id="BTC-USDT-PERP",
        bid_price=Decimal("65000.0"),
        ask_price=Decimal("65000.5"),
        observed_timestamp=100.0,
    )

    with pytest.raises(ValueError, match="same venue and instrument"):
        policies_module.evaluate_checker_policies(
            checker_book,
            reference_book,
            now_timestamp=101.0,
        )
