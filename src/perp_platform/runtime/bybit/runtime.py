from __future__ import annotations

from dataclasses import dataclass

from .clients import BybitExecutionClient, BybitStreamClient
from .config import BybitRuntimeConfig


@dataclass(frozen=True)
class BybitRuntimeWiring:
    public_stream: BybitStreamClient
    private_stream: BybitStreamClient | None
    execution_client: BybitExecutionClient


def wire_bybit_runtime(config: BybitRuntimeConfig) -> BybitRuntimeWiring:
    private_enabled = bool(config.api_key and config.api_secret)

    return BybitRuntimeWiring(
        public_stream=BybitStreamClient(
            channel="public",
            url=config.public_ws_url,
            category=config.category,
            requires_auth=False,
        ),
        private_stream=(
            BybitStreamClient(
                channel="private",
                url=config.private_ws_url,
                category=config.category,
                requires_auth=True,
            )
            if private_enabled
            else None
        ),
        execution_client=BybitExecutionClient(
            rest_base_url=config.rest_base_url,
            category=config.category,
            settle_coin=config.settle_coin,
            api_key_present=bool(config.api_key),
            api_secret_present=bool(config.api_secret),
        ),
    )
