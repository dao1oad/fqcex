from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from ...config import AppConfig, load_config
from .config import BybitRuntimeConfig, load_bybit_runtime_config
from .guards import BybitRuntimeGuards, build_bybit_runtime_guards
from .runtime import BybitRuntimeWiring, wire_bybit_runtime


@dataclass(frozen=True)
class BybitRuntimeBootstrapResult:
    app_config: AppConfig
    runtime_config: BybitRuntimeConfig
    runtime: BybitRuntimeWiring
    guards: BybitRuntimeGuards
    client_label: str
    private_client_enabled: bool


def bootstrap_bybit_runtime(
    environ: Mapping[str, str] | None = None,
) -> BybitRuntimeBootstrapResult:
    app_config = load_config(environ)
    runtime_config = load_bybit_runtime_config(environ)

    runtime = wire_bybit_runtime(runtime_config)
    guards = build_bybit_runtime_guards()

    return BybitRuntimeBootstrapResult(
        app_config=app_config,
        runtime_config=runtime_config,
        runtime=runtime,
        guards=guards,
        client_label=f"bybit-{runtime_config.category}-{runtime_config.environment}",
        private_client_enabled=bool(
            runtime_config.api_key and runtime_config.api_secret
        ),
    )
