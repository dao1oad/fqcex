from __future__ import annotations

from tests.perp_platform.support.config import import_perp_platform_module


def test_wire_bybit_runtime_without_credentials_disables_private_stream() -> None:
    config_module = import_perp_platform_module("perp_platform.runtime.bybit.config")
    runtime_module = import_perp_platform_module("perp_platform.runtime.bybit.runtime")

    config = config_module.BybitRuntimeConfig(
        environment="testnet",
        api_key="",
        api_secret="",
        category="linear",
        settle_coin="USDT",
        rest_base_url="https://api-testnet.bybit.example",
        public_ws_url="wss://public-testnet.bybit.example",
        private_ws_url="wss://private-testnet.bybit.example",
    )

    wiring = runtime_module.wire_bybit_runtime(config)

    assert wiring.public_stream == runtime_module.BybitStreamClient(
        channel="public",
        url="wss://public-testnet.bybit.example",
        category="linear",
        requires_auth=False,
    )
    assert wiring.private_stream is None
    assert wiring.execution_client == runtime_module.BybitExecutionClient(
        rest_base_url="https://api-testnet.bybit.example",
        category="linear",
        settle_coin="USDT",
        api_key_present=False,
        api_secret_present=False,
    )


def test_wire_bybit_runtime_with_credentials_enables_private_stream() -> None:
    config_module = import_perp_platform_module("perp_platform.runtime.bybit.config")
    runtime_module = import_perp_platform_module("perp_platform.runtime.bybit.runtime")

    config = config_module.BybitRuntimeConfig(
        environment="mainnet",
        api_key="key-123",
        api_secret="secret-456",
        category="linear",
        settle_coin="USDT",
        rest_base_url="https://api.bybit.example",
        public_ws_url="wss://public.bybit.example",
        private_ws_url="wss://private.bybit.example",
    )

    wiring = runtime_module.wire_bybit_runtime(config)

    assert wiring.private_stream == runtime_module.BybitStreamClient(
        channel="private",
        url="wss://private.bybit.example",
        category="linear",
        requires_auth=True,
    )
    assert wiring.execution_client.rest_base_url == "https://api.bybit.example"
    assert wiring.execution_client.category == "linear"
    assert wiring.execution_client.settle_coin == "USDT"
    assert wiring.execution_client.api_key_present is True
    assert wiring.execution_client.api_secret_present is True
