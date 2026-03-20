from __future__ import annotations

from tests.perp_platform.support.config import import_perp_platform_module


def test_bootstrap_smoke_exposes_runtime_and_guards() -> None:
    bootstrap_module = import_perp_platform_module("perp_platform.runtime.bybit.bootstrap")

    result = bootstrap_module.bootstrap_bybit_runtime(
        {
            "BYBIT_ENVIRONMENT": "testnet",
            "BYBIT_API_KEY": "key-123",
            "BYBIT_API_SECRET": "secret-456",
        }
    )

    assert result.runtime.public_stream is not None
    assert result.runtime.execution_client is not None
    assert result.guards is not None
    assert result.private_client_enabled is True
