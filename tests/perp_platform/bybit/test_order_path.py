from __future__ import annotations

import pytest

from tests.perp_platform.support.config import import_perp_platform_module


def _bootstrap_with_private_credentials():
    bootstrap_module = import_perp_platform_module("perp_platform.runtime.bybit.bootstrap")
    return bootstrap_module.bootstrap_bybit_runtime(
        {
            "BYBIT_ENVIRONMENT": "testnet",
            "BYBIT_API_KEY": "key-123",
            "BYBIT_API_SECRET": "secret-456",
        }
    )


@pytest.mark.parametrize(
    ("order_type", "time_in_force", "reduce_only"),
    [("LIMIT", "GTC", False), ("MARKET", "IOC", True)],
)
def test_build_bybit_order_path_accepts_allowed_order_capabilities(
    order_type: str,
    time_in_force: str,
    reduce_only: bool,
) -> None:
    order_path_module = import_perp_platform_module("perp_platform.runtime.bybit.order_path")
    bootstrap_result = _bootstrap_with_private_credentials()

    order_path = order_path_module.build_bybit_order_path(
        order_type=order_type,
        time_in_force=time_in_force,
        reduce_only=reduce_only,
        bootstrap_result=bootstrap_result,
    )

    assert order_path.rest_base_url == bootstrap_result.runtime.execution_client.rest_base_url
    assert order_path.category == bootstrap_result.runtime.execution_client.category
    assert order_path.settle_coin == bootstrap_result.runtime.execution_client.settle_coin
    assert order_path.order_type == order_type
    assert order_path.time_in_force == time_in_force
    assert order_path.reduce_only == reduce_only
    assert order_path.private_client_required is True


@pytest.mark.parametrize(
    ("order_type", "time_in_force"),
    [("STOP", "GTC"), ("LIMIT", "FOK")],
)
def test_build_bybit_order_path_rejects_invalid_order_capabilities(
    order_type: str,
    time_in_force: str,
) -> None:
    order_path_module = import_perp_platform_module("perp_platform.runtime.bybit.order_path")
    bootstrap_result = _bootstrap_with_private_credentials()

    with pytest.raises(ValueError):
        order_path_module.build_bybit_order_path(
            order_type=order_type,
            time_in_force=time_in_force,
            reduce_only=False,
            bootstrap_result=bootstrap_result,
        )
