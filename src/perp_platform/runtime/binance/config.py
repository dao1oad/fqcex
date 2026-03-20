from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

ALLOWED_BINANCE_ENVIRONMENTS = frozenset({"testnet", "mainnet"})

DEFAULT_ENDPOINTS = {
    "testnet": {
        "rest_base_url": "https://testnet.binancefuture.com",
        "public_ws_url": "wss://stream.binancefuture.com/ws",
        "private_ws_url": "wss://stream.binancefuture.com/ws",
    },
    "mainnet": {
        "rest_base_url": "https://fapi.binance.com",
        "public_ws_url": "wss://fstream.binance.com/ws",
        "private_ws_url": "wss://fstream.binance.com/ws",
    },
}


@dataclass(frozen=True)
class BinanceRuntimeConfig:
    environment: str
    api_key: str
    api_secret: str
    market: str
    settle_asset: str
    rest_base_url: str
    public_ws_url: str
    private_ws_url: str


def load_binance_runtime_config(
    environ: Mapping[str, str] | None = None,
) -> BinanceRuntimeConfig:
    source = {} if environ is None else environ
    environment = source.get("BINANCE_ENVIRONMENT", "testnet").strip().lower()

    if environment not in ALLOWED_BINANCE_ENVIRONMENTS:
        raise ValueError("BINANCE_ENVIRONMENT must be one of: testnet, mainnet")

    defaults = DEFAULT_ENDPOINTS[environment]

    return BinanceRuntimeConfig(
        environment=environment,
        api_key=source.get("BINANCE_API_KEY", "").strip(),
        api_secret=source.get("BINANCE_API_SECRET", "").strip(),
        market="usdm",
        settle_asset="USDT",
        rest_base_url=source.get(
            "BINANCE_REST_BASE_URL", defaults["rest_base_url"]
        ).strip(),
        public_ws_url=source.get(
            "BINANCE_PUBLIC_WS_URL", defaults["public_ws_url"]
        ).strip(),
        private_ws_url=source.get(
            "BINANCE_PRIVATE_WS_URL", defaults["private_ws_url"]
        ).strip(),
    )
