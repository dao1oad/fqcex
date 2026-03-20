from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

ALLOWED_OKX_ENVIRONMENTS = frozenset({"demo", "mainnet"})

DEFAULT_ENDPOINTS = {
    "demo": {
        "rest_base_url": "https://www.okx.com",
        "public_ws_url": "wss://wspap.okx.com:8443/ws/v5/public",
        "private_ws_url": "wss://wspap.okx.com:8443/ws/v5/private",
    },
    "mainnet": {
        "rest_base_url": "https://www.okx.com",
        "public_ws_url": "wss://ws.okx.com:8443/ws/v5/public",
        "private_ws_url": "wss://ws.okx.com:8443/ws/v5/private",
    },
}


@dataclass(frozen=True)
class OkxRuntimeConfig:
    environment: str
    api_key: str
    api_secret: str
    api_passphrase: str
    instrument_type: str
    settle_asset: str
    rest_base_url: str
    public_ws_url: str
    private_ws_url: str


def load_okx_runtime_config(
    environ: Mapping[str, str] | None = None,
) -> OkxRuntimeConfig:
    source = {} if environ is None else environ
    environment = source.get("OKX_ENVIRONMENT", "demo").strip().lower()

    if environment not in ALLOWED_OKX_ENVIRONMENTS:
        raise ValueError("OKX_ENVIRONMENT must be one of: demo, mainnet")

    defaults = DEFAULT_ENDPOINTS[environment]

    return OkxRuntimeConfig(
        environment=environment,
        api_key=source.get("OKX_API_KEY", "").strip(),
        api_secret=source.get("OKX_API_SECRET", "").strip(),
        api_passphrase=source.get("OKX_API_PASSPHRASE", "").strip(),
        instrument_type="SWAP",
        settle_asset="USDT",
        rest_base_url=source.get("OKX_REST_BASE_URL", defaults["rest_base_url"]).strip(),
        public_ws_url=source.get("OKX_PUBLIC_WS_URL", defaults["public_ws_url"]).strip(),
        private_ws_url=source.get("OKX_PRIVATE_WS_URL", defaults["private_ws_url"]).strip(),
    )
