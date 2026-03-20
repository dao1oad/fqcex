from __future__ import annotations

import pytest

from tests.perp_platform.support.config import import_perp_platform_module


def test_load_binance_runtime_config_reads_environment() -> None:
    config_module = import_perp_platform_module("perp_platform.runtime.binance.config")

    config = config_module.load_binance_runtime_config(
        {
            "BINANCE_ENVIRONMENT": "mainnet",
            "BINANCE_API_KEY": "key-123",
            "BINANCE_API_SECRET": "secret-456",
            "BINANCE_REST_BASE_URL": "https://fapi.binance.example",
            "BINANCE_PUBLIC_WS_URL": "wss://public.binance.example/ws",
            "BINANCE_PRIVATE_WS_URL": "wss://private.binance.example/ws",
        }
    )

    assert config == config_module.BinanceRuntimeConfig(
        environment="mainnet",
        api_key="key-123",
        api_secret="secret-456",
        market="usdm",
        settle_asset="USDT",
        rest_base_url="https://fapi.binance.example",
        public_ws_url="wss://public.binance.example/ws",
        private_ws_url="wss://private.binance.example/ws",
    )


def test_load_binance_runtime_config_rejects_invalid_environment() -> None:
    config_module = import_perp_platform_module("perp_platform.runtime.binance.config")

    with pytest.raises(ValueError, match="BINANCE_ENVIRONMENT"):
        config_module.load_binance_runtime_config({"BINANCE_ENVIRONMENT": "sandbox"})


def test_bootstrap_binance_runtime_returns_stable_result() -> None:
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
    assert result.app_config.environment == "test"
    assert result.runtime_config.environment == "testnet"
    assert result.runtime_config.market == "usdm"
    assert result.runtime_config.settle_asset == "USDT"
    assert result.client_targets.rest_base_url == "https://testnet.binancefuture.com"
    assert result.client_targets.public_ws_url == "wss://stream.binancefuture.com/ws"
    assert result.client_targets.private_ws_url == "wss://stream.binancefuture.com/ws"


def test_bootstrap_binance_runtime_disables_private_client_without_credentials() -> (
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
