from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

ALLOWED_BYBIT_ENVIRONMENTS = frozenset({"testnet", "mainnet"})

DEFAULT_ENDPOINTS = {
    "testnet": {
        "rest_base_url": "https://api-testnet.bybit.com",
        "public_ws_url": "wss://stream-testnet.bybit.com/v5/public/linear",
        "private_ws_url": "wss://stream-testnet.bybit.com/v5/private",
    },
    "mainnet": {
        "rest_base_url": "https://api.bybit.com",
        "public_ws_url": "wss://stream.bybit.com/v5/public/linear",
        "private_ws_url": "wss://stream.bybit.com/v5/private",
    },
}


@dataclass(frozen=True)
class BybitRuntimeConfig:
    environment: str
    api_key: str
    api_secret: str
    category: str
    settle_coin: str
    rest_base_url: str
    public_ws_url: str
    private_ws_url: str


def load_bybit_runtime_config(
    environ: Mapping[str, str] | None = None,
) -> BybitRuntimeConfig:
    source = {} if environ is None else environ
    environment = source.get("BYBIT_ENVIRONMENT", "testnet").strip().lower()

    if environment not in ALLOWED_BYBIT_ENVIRONMENTS:
        raise ValueError("BYBIT_ENVIRONMENT must be one of: testnet, mainnet")

    defaults = DEFAULT_ENDPOINTS[environment]

    return BybitRuntimeConfig(
        environment=environment,
        api_key=source.get("BYBIT_API_KEY", "").strip(),
        api_secret=source.get("BYBIT_API_SECRET", "").strip(),
        category="linear",
        settle_coin="USDT",
        rest_base_url=source.get("BYBIT_REST_BASE_URL", defaults["rest_base_url"]).strip(),
        public_ws_url=source.get("BYBIT_PUBLIC_WS_URL", defaults["public_ws_url"]).strip(),
        private_ws_url=source.get(
            "BYBIT_PRIVATE_WS_URL", defaults["private_ws_url"]
        ).strip(),
    )
