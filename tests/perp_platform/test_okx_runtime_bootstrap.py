from __future__ import annotations

import pytest

from tests.perp_platform.support.config import import_perp_platform_module


def test_load_okx_runtime_config_reads_environment() -> None:
    config_module = import_perp_platform_module("perp_platform.runtime.okx.config")

    config = config_module.load_okx_runtime_config(
        {
            "OKX_ENVIRONMENT": "mainnet",
            "OKX_API_KEY": "key-123",
            "OKX_API_SECRET": "secret-456",
            "OKX_API_PASSPHRASE": "pass-789",
            "OKX_REST_BASE_URL": "https://okx.example",
            "OKX_PUBLIC_WS_URL": "wss://public.okx.example/ws",
            "OKX_PRIVATE_WS_URL": "wss://private.okx.example/ws",
        }
    )

    assert config == config_module.OkxRuntimeConfig(
        environment="mainnet",
        api_key="key-123",
        api_secret="secret-456",
        api_passphrase="pass-789",
        instrument_type="SWAP",
        settle_asset="USDT",
        rest_base_url="https://okx.example",
        public_ws_url="wss://public.okx.example/ws",
        private_ws_url="wss://private.okx.example/ws",
    )


def test_load_okx_runtime_config_rejects_invalid_environment() -> None:
    config_module = import_perp_platform_module("perp_platform.runtime.okx.config")

    with pytest.raises(ValueError, match="OKX_ENVIRONMENT"):
        config_module.load_okx_runtime_config({"OKX_ENVIRONMENT": "sandbox"})


def test_bootstrap_okx_runtime_returns_stable_result() -> None:
    bootstrap_module = import_perp_platform_module("perp_platform.runtime.okx.bootstrap")

    result = bootstrap_module.bootstrap_okx_runtime(
        {
            "PERP_PLATFORM_APP_NAME": "perp-platform",
            "PERP_PLATFORM_ENVIRONMENT": "test",
            "PERP_PLATFORM_LOG_LEVEL": "INFO",
            "OKX_ENVIRONMENT": "demo",
            "OKX_API_KEY": "key-123",
            "OKX_API_SECRET": "secret-456",
            "OKX_API_PASSPHRASE": "pass-789",
        }
    )

    assert result.client_label == "okx-swap-demo"
    assert result.private_client_enabled is True
    assert result.app_config.environment == "test"
    assert result.runtime_config.environment == "demo"
    assert result.runtime_config.instrument_type == "SWAP"
    assert result.runtime_config.settle_asset == "USDT"
    assert result.client_targets.rest_base_url == "https://www.okx.com"
    assert result.client_targets.public_ws_url == "wss://wspap.okx.com:8443/ws/v5/public"
    assert result.client_targets.private_ws_url == "wss://wspap.okx.com:8443/ws/v5/private"
    assert result.runtime.rest_base_url == "https://www.okx.com"
    assert result.runtime.public_ws_url == "wss://wspap.okx.com:8443/ws/v5/public"
    assert result.runtime.private_ws_url == "wss://wspap.okx.com:8443/ws/v5/private"
    assert result.runtime.position_mode == "net"
    assert result.runtime.margin_mode == "isolated"
    assert result.guards.position_mode == "net"
    assert result.guards.margin_mode == "isolated"


def test_bootstrap_okx_runtime_requires_key_secret_and_passphrase_for_private_client() -> (
    None
):
    bootstrap_module = import_perp_platform_module("perp_platform.runtime.okx.bootstrap")

    result = bootstrap_module.bootstrap_okx_runtime(
        {
            "PERP_PLATFORM_APP_NAME": "perp-platform",
            "PERP_PLATFORM_ENVIRONMENT": "dev",
            "PERP_PLATFORM_LOG_LEVEL": "INFO",
            "OKX_ENVIRONMENT": "mainnet",
            "OKX_API_KEY": "key-123",
            "OKX_API_SECRET": "secret-456",
        }
    )

    assert result.client_label == "okx-swap-mainnet"
    assert result.private_client_enabled is False
    assert result.runtime.private_ws_url is None
