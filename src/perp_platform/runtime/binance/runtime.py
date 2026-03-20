from __future__ import annotations

from dataclasses import dataclass

from .clients import BinanceExecutionClient, BinanceStreamClient
from .config import BinanceRuntimeConfig


@dataclass(frozen=True)
class BinanceRuntimeWiring:
    public_stream: BinanceStreamClient
    private_stream: BinanceStreamClient | None
    execution_client: BinanceExecutionClient


def wire_binance_runtime(config: BinanceRuntimeConfig) -> BinanceRuntimeWiring:
    private_enabled = bool(config.api_key and config.api_secret)

    return BinanceRuntimeWiring(
        public_stream=BinanceStreamClient(
            channel="public",
            url=config.public_ws_url,
            market=config.market,
            requires_auth=False,
        ),
        private_stream=(
            BinanceStreamClient(
                channel="private",
                url=config.private_ws_url,
                market=config.market,
                requires_auth=True,
            )
            if private_enabled
            else None
        ),
        execution_client=BinanceExecutionClient(
            rest_base_url=config.rest_base_url,
            market=config.market,
            settle_asset=config.settle_asset,
            api_key_present=bool(config.api_key),
            api_secret_present=bool(config.api_secret),
        ),
    )
