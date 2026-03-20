from __future__ import annotations

import pytest

from tests.perp_platform.support.config import import_perp_platform_module


def test_load_checker_config_reads_environment() -> None:
    config_module = import_perp_platform_module("perp_platform.checker.config")
    instruments_module = import_perp_platform_module("perp_platform.domain.instruments")

    config = config_module.load_checker_config(
        {
            "CHECKER_SERVICE_NAME": "market-checker",
            "CHECKER_VENUES": "BYBIT, BINANCE",
            "CHECKER_INSTRUMENTS": "BTC-USDT-PERP, ETH-USDT-PERP",
        }
    )

    assert config == config_module.CheckerConfig(
        service_name="market-checker",
        venues=(instruments_module.Venue.BYBIT, instruments_module.Venue.BINANCE),
        instrument_ids=("BTC-USDT-PERP", "ETH-USDT-PERP"),
    )


def test_load_checker_config_rejects_invalid_venue() -> None:
    config_module = import_perp_platform_module("perp_platform.checker.config")

    with pytest.raises(ValueError, match="CHECKER_VENUES"):
        config_module.load_checker_config({"CHECKER_VENUES": "BYBIT,KRAKEN"})


def test_load_checker_config_rejects_non_usdt_perp_instrument() -> None:
    config_module = import_perp_platform_module("perp_platform.checker.config")

    with pytest.raises(ValueError, match="CHECKER_INSTRUMENTS"):
        config_module.load_checker_config({"CHECKER_INSTRUMENTS": "BTC-USDC-PERP"})


def test_bootstrap_checker_returns_stable_subscription_plan() -> None:
    checker_module = import_perp_platform_module("perp_platform.checker.bootstrap")
    instruments_module = import_perp_platform_module("perp_platform.domain.instruments")

    result = checker_module.bootstrap_checker(
        {
            "PERP_PLATFORM_APP_NAME": "perp-platform",
            "PERP_PLATFORM_ENVIRONMENT": "test",
            "PERP_PLATFORM_LOG_LEVEL": "INFO",
        }
    )

    assert result.service_label == "cryptofeed-checker-test"
    assert result.checker_config.service_name == "cryptofeed-checker"
    assert result.checker_config.venues == (
        instruments_module.Venue.BYBIT,
        instruments_module.Venue.BINANCE,
        instruments_module.Venue.OKX,
    )
    assert result.checker_config.instrument_ids == ("BTC-USDT-PERP", "ETH-USDT-PERP")
    assert len(result.subscription_plan) == 6
    assert result.subscription_plan[0] == checker_module.CheckerSubscriptionTarget(
        venue=instruments_module.Venue.BYBIT,
        instrument_id="BTC-USDT-PERP",
    )
