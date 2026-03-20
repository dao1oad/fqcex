from __future__ import annotations

from tests.perp_platform.support.config import import_perp_platform_module


def test_wire_binance_runtime_without_credentials_disables_private_stream() -> None:
    config_module = import_perp_platform_module("perp_platform.runtime.binance.config")
    runtime_module = import_perp_platform_module("perp_platform.runtime.binance.runtime")

    config = config_module.BinanceRuntimeConfig(
        environment="testnet",
        api_key="",
        api_secret="",
        market="usdm",
        settle_asset="USDT",
        rest_base_url="https://testnet.binancefuture.example",
        public_ws_url="wss://public-testnet.binance.example/ws",
        private_ws_url="wss://private-testnet.binance.example/ws",
    )

    wiring = runtime_module.wire_binance_runtime(config)

    assert wiring.public_stream == runtime_module.BinanceStreamClient(
        channel="public",
        url="wss://public-testnet.binance.example/ws",
        market="usdm",
        requires_auth=False,
    )
    assert wiring.private_stream is None
    assert wiring.execution_client == runtime_module.BinanceExecutionClient(
        rest_base_url="https://testnet.binancefuture.example",
        market="usdm",
        settle_asset="USDT",
        api_key_present=False,
        api_secret_present=False,
    )


def test_wire_binance_runtime_with_credentials_enables_private_stream() -> None:
    config_module = import_perp_platform_module("perp_platform.runtime.binance.config")
    runtime_module = import_perp_platform_module("perp_platform.runtime.binance.runtime")

    config = config_module.BinanceRuntimeConfig(
        environment="mainnet",
        api_key="key-123",
        api_secret="secret-456",
        market="usdm",
        settle_asset="USDT",
        rest_base_url="https://fapi.binance.example",
        public_ws_url="wss://public.binance.example/ws",
        private_ws_url="wss://private.binance.example/ws",
    )

    wiring = runtime_module.wire_binance_runtime(config)

    assert wiring.private_stream == runtime_module.BinanceStreamClient(
        channel="private",
        url="wss://private.binance.example/ws",
        market="usdm",
        requires_auth=True,
    )
    assert wiring.execution_client.rest_base_url == "https://fapi.binance.example"
    assert wiring.execution_client.market == "usdm"
    assert wiring.execution_client.settle_asset == "USDT"
    assert wiring.execution_client.api_key_present is True
    assert wiring.execution_client.api_secret_present is True
