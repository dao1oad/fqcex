from __future__ import annotations

import pytest

from tests.perp_platform.support.config import import_perp_platform_module


@pytest.fixture
def guards_module():
    return import_perp_platform_module("perp_platform.runtime.okx.guards")


def test_build_okx_runtime_guards_returns_phase1_constraints(guards_module) -> None:
    guards = guards_module.build_okx_runtime_guards()

    assert guards.position_mode == "net"
    assert guards.margin_mode == "isolated"
    assert guards.default_leverage == 2
    assert guards.max_leverage == 3
    assert guards.allowed_order_types == ("LIMIT", "MARKET")
    assert guards.allowed_time_in_force == ("GTC", "IOC")
    assert guards.reduce_only_supported is True


def test_validate_okx_leverage_accepts_default_and_upper_bound(guards_module) -> None:
    guards = guards_module.build_okx_runtime_guards()

    guards_module.validate_okx_leverage(2, guards)
    guards_module.validate_okx_leverage(3, guards)


@pytest.mark.parametrize("invalid_leverage", [0, 4])
def test_validate_okx_leverage_rejects_out_of_bound_values(
    guards_module, invalid_leverage: int
) -> None:
    guards = guards_module.build_okx_runtime_guards()

    with pytest.raises(ValueError):
        guards_module.validate_okx_leverage(invalid_leverage, guards)


@pytest.mark.parametrize(
    ("order_type", "time_in_force", "reduce_only"),
    [("LIMIT", "GTC", False), ("LIMIT", "IOC", True), ("MARKET", "IOC", True)],
)
def test_validate_okx_order_capability_accepts_allowed_modes(
    guards_module,
    order_type: str,
    time_in_force: str,
    reduce_only: bool,
) -> None:
    guards = guards_module.build_okx_runtime_guards()

    guards_module.validate_okx_order_capability(
        order_type=order_type,
        time_in_force=time_in_force,
        reduce_only=reduce_only,
        guards=guards,
    )


@pytest.mark.parametrize(
    ("order_type", "time_in_force", "message"),
    [
        ("STOP", "GTC", "order_type"),
        ("LIMIT", "FOK", "time_in_force"),
        ("MARKET", "GTC", "MARKET"),
    ],
)
def test_validate_okx_order_capability_rejects_invalid_combinations(
    guards_module,
    order_type: str,
    time_in_force: str,
    message: str,
) -> None:
    guards = guards_module.build_okx_runtime_guards()

    with pytest.raises(ValueError, match=message):
        guards_module.validate_okx_order_capability(
            order_type=order_type,
            time_in_force=time_in_force,
            reduce_only=False,
            guards=guards,
        )
