from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from ...config import AppConfig, load_config
from .config import BinanceRuntimeConfig, load_binance_runtime_config
from .runtime import BinanceRuntimeWiring, wire_binance_runtime


@dataclass(frozen=True)
class BinanceClientTargets:
    rest_base_url: str
    public_ws_url: str
    private_ws_url: str


@dataclass(frozen=True)
class BinanceRuntimeBootstrapResult:
    app_config: AppConfig
    runtime_config: BinanceRuntimeConfig
    client_targets: BinanceClientTargets
    runtime: BinanceRuntimeWiring
    client_label: str
    private_client_enabled: bool


def bootstrap_binance_runtime(
    environ: Mapping[str, str] | None = None,
) -> BinanceRuntimeBootstrapResult:
    app_config = load_config(environ)
    runtime_config = load_binance_runtime_config(environ)
    runtime = wire_binance_runtime(runtime_config)

    return BinanceRuntimeBootstrapResult(
        app_config=app_config,
        runtime_config=runtime_config,
        client_targets=BinanceClientTargets(
            rest_base_url=runtime_config.rest_base_url,
            public_ws_url=runtime_config.public_ws_url,
            private_ws_url=runtime_config.private_ws_url,
        ),
        runtime=runtime,
        client_label=f"binance-{runtime_config.market}-{runtime_config.environment}",
        private_client_enabled=bool(
            runtime_config.api_key and runtime_config.api_secret
        ),
    )
