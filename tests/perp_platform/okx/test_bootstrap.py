from __future__ import annotations

from tests.perp_platform.support.config import import_perp_platform_module


def test_okx_package_bootstrap_exposes_runtime_and_guards() -> None:
    okx = import_perp_platform_module("perp_platform.runtime.okx")

    result = okx.bootstrap_okx_runtime(
        {
            "PERP_PLATFORM_APP_NAME": "perp-platform",
            "PERP_PLATFORM_ENVIRONMENT": "test",
            "PERP_PLATFORM_LOG_LEVEL": "INFO",
            "OKX_ENVIRONMENT": "demo",
            "OKX_API_KEY": "key-123",
            "OKX_API_SECRET": "secret-456",
            "OKX_API_PASSPHRASE": "pass-789",
        }
    )

    assert result.client_label == "okx-swap-demo"
    assert result.private_client_enabled is True
    assert result.runtime.position_mode == "net"
    assert result.runtime.margin_mode == "isolated"
    assert result.guards.position_mode == "net"
    assert result.guards.margin_mode == "isolated"


def test_okx_package_bootstrap_without_full_private_credentials_disables_private_path() -> (
    None
):
    okx = import_perp_platform_module("perp_platform.runtime.okx")

    result = okx.bootstrap_okx_runtime(
        {
            "PERP_PLATFORM_APP_NAME": "perp-platform",
            "PERP_PLATFORM_ENVIRONMENT": "dev",
            "PERP_PLATFORM_LOG_LEVEL": "INFO",
            "OKX_ENVIRONMENT": "mainnet",
            "OKX_API_KEY": "key-123",
            "OKX_API_SECRET": "secret-456",
        }
    )

    assert result.client_label == "okx-swap-mainnet"
    assert result.private_client_enabled is False
    assert result.runtime.private_ws_url is None
