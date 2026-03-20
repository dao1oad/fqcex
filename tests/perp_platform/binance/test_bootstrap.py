from __future__ import annotations

from tests.perp_platform.support.config import import_perp_platform_module


def test_bootstrap_binance_runtime_smoke_matches_runtime_and_targets() -> None:
    bootstrap_module = import_perp_platform_module(
        "perp_platform.runtime.binance.bootstrap"
    )

    result = bootstrap_module.bootstrap_binance_runtime(
        {
            "PERP_PLATFORM_APP_NAME": "perp-platform",
            "PERP_PLATFORM_ENVIRONMENT": "test",
            "PERP_PLATFORM_LOG_LEVEL": "INFO",
            "BINANCE_ENVIRONMENT": "testnet",
            "BINANCE_API_KEY": "key-123",
            "BINANCE_API_SECRET": "secret-456",
        }
    )

    assert result.client_label == "binance-usdm-testnet"
    assert result.private_client_enabled is True
    assert result.runtime.public_stream.url == result.client_targets.public_ws_url
    assert result.runtime.private_stream is not None
    assert result.runtime.private_stream.url == result.client_targets.private_ws_url
    assert result.runtime.execution_client.rest_base_url == result.client_targets.rest_base_url


def test_bootstrap_binance_runtime_mainnet_without_credentials_stays_public_only() -> (
    None
):
    bootstrap_module = import_perp_platform_module(
        "perp_platform.runtime.binance.bootstrap"
    )

    result = bootstrap_module.bootstrap_binance_runtime(
        {
            "PERP_PLATFORM_APP_NAME": "perp-platform",
            "PERP_PLATFORM_ENVIRONMENT": "dev",
            "PERP_PLATFORM_LOG_LEVEL": "INFO",
            "BINANCE_ENVIRONMENT": "mainnet",
        }
    )

    assert result.client_label == "binance-usdm-mainnet"
    assert result.private_client_enabled is False
    assert result.runtime.public_stream.url == "wss://fstream.binance.com/ws"
    assert result.runtime.private_stream is None
    assert result.runtime.execution_client.market == "usdm"
    assert result.runtime.execution_client.settle_asset == "USDT"
