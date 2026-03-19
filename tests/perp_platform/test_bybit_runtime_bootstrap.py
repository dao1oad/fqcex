from __future__ import annotations

import pytest

from tests.perp_platform.support.config import import_perp_platform_module


def test_load_bybit_runtime_config_reads_environment() -> None:
    config_module = import_perp_platform_module("perp_platform.runtime.bybit.config")

    config = config_module.load_bybit_runtime_config(
        {
            "BYBIT_ENVIRONMENT": "mainnet",
            "BYBIT_API_KEY": "key-123",
            "BYBIT_API_SECRET": "secret-456",
            "BYBIT_REST_BASE_URL": "https://api.bybit.example",
            "BYBIT_PUBLIC_WS_URL": "wss://public.bybit.example",
            "BYBIT_PRIVATE_WS_URL": "wss://private.bybit.example",
        }
    )

    assert config == config_module.BybitRuntimeConfig(
        environment="mainnet",
        api_key="key-123",
        api_secret="secret-456",
        category="linear",
        settle_coin="USDT",
        rest_base_url="https://api.bybit.example",
        public_ws_url="wss://public.bybit.example",
        private_ws_url="wss://private.bybit.example",
    )


def test_load_bybit_runtime_config_rejects_invalid_environment() -> None:
    config_module = import_perp_platform_module("perp_platform.runtime.bybit.config")

    with pytest.raises(ValueError, match="BYBIT_ENVIRONMENT"):
        config_module.load_bybit_runtime_config({"BYBIT_ENVIRONMENT": "sandbox"})


def test_bootstrap_bybit_runtime_returns_stable_result() -> None:
    bootstrap_module = import_perp_platform_module("perp_platform.runtime.bybit.bootstrap")

    result = bootstrap_module.bootstrap_bybit_runtime(
        {
            "PERP_PLATFORM_APP_NAME": "perp-platform",
            "PERP_PLATFORM_ENVIRONMENT": "test",
            "PERP_PLATFORM_LOG_LEVEL": "INFO",
            "BYBIT_ENVIRONMENT": "testnet",
            "BYBIT_API_KEY": "key-123",
            "BYBIT_API_SECRET": "secret-456",
        }
    )

    assert result.client_label == "bybit-linear-testnet"
    assert result.private_client_enabled is True
    assert result.app_config.environment == "test"
    assert result.runtime_config.environment == "testnet"
    assert result.runtime_config.category == "linear"
    assert result.runtime_config.settle_coin == "USDT"
    assert result.runtime_config.rest_base_url == "https://api-testnet.bybit.com"
    assert result.runtime.public_stream.channel == "public"
    assert result.runtime.public_stream.url == "wss://stream-testnet.bybit.com/v5/public/linear"
    assert result.runtime.execution_client.rest_base_url == "https://api-testnet.bybit.com"
