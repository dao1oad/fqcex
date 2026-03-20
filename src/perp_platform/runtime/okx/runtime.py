from __future__ import annotations

from dataclasses import dataclass

from .config import OkxRuntimeConfig
from .guards import OkxRuntimeGuards


@dataclass(frozen=True)
class OkxRuntimeWiring:
    rest_base_url: str
    public_ws_url: str
    private_ws_url: str | None
    instrument_type: str
    settle_asset: str
    position_mode: str
    margin_mode: str


def wire_okx_runtime(
    config: OkxRuntimeConfig,
    guards: OkxRuntimeGuards,
) -> OkxRuntimeWiring:
    private_enabled = bool(config.api_key and config.api_secret and config.api_passphrase)

    return OkxRuntimeWiring(
        rest_base_url=config.rest_base_url,
        public_ws_url=config.public_ws_url,
        private_ws_url=config.private_ws_url if private_enabled else None,
        instrument_type=config.instrument_type,
        settle_asset=config.settle_asset,
        position_mode=guards.position_mode,
        margin_mode=guards.margin_mode,
    )
