from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from ...config import AppConfig, load_config
from .config import OkxRuntimeConfig, load_okx_runtime_config
from .guards import OkxRuntimeGuards, build_okx_runtime_guards
from .runtime import OkxRuntimeWiring, wire_okx_runtime


@dataclass(frozen=True)
class OkxClientTargets:
    rest_base_url: str
    public_ws_url: str
    private_ws_url: str


@dataclass(frozen=True)
class OkxRuntimeBootstrapResult:
    app_config: AppConfig
    runtime_config: OkxRuntimeConfig
    client_targets: OkxClientTargets
    runtime: OkxRuntimeWiring
    guards: OkxRuntimeGuards
    client_label: str
    private_client_enabled: bool


def bootstrap_okx_runtime(
    environ: Mapping[str, str] | None = None,
) -> OkxRuntimeBootstrapResult:
    app_config = load_config(environ)
    runtime_config = load_okx_runtime_config(environ)
    guards = build_okx_runtime_guards()
    runtime = wire_okx_runtime(runtime_config, guards)

    return OkxRuntimeBootstrapResult(
        app_config=app_config,
        runtime_config=runtime_config,
        client_targets=OkxClientTargets(
            rest_base_url=runtime_config.rest_base_url,
            public_ws_url=runtime_config.public_ws_url,
            private_ws_url=runtime_config.private_ws_url,
        ),
        runtime=runtime,
        guards=guards,
        client_label=f"okx-{runtime_config.instrument_type.lower()}-{runtime_config.environment}",
        private_client_enabled=bool(
            runtime_config.api_key
            and runtime_config.api_secret
            and runtime_config.api_passphrase
        ),
    )
