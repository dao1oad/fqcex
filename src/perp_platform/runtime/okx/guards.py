from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class OkxRuntimeGuards:
    position_mode: str
    margin_mode: str
    default_leverage: int
    max_leverage: int
    allowed_order_types: tuple[str, ...]
    allowed_time_in_force: tuple[str, ...]
    reduce_only_supported: bool


def build_okx_runtime_guards() -> OkxRuntimeGuards:
    return OkxRuntimeGuards(
        position_mode="net",
        margin_mode="isolated",
        default_leverage=2,
        max_leverage=3,
        allowed_order_types=("LIMIT", "MARKET"),
        allowed_time_in_force=("GTC", "IOC"),
        reduce_only_supported=True,
    )


def validate_okx_leverage(leverage: int, guards: OkxRuntimeGuards) -> None:
    if leverage < 1:
        raise ValueError("OKX leverage must be >= 1")
    if leverage > guards.max_leverage:
        raise ValueError(f"OKX leverage {leverage} exceeds max leverage {guards.max_leverage}")


def validate_okx_order_capability(
    order_type: str,
    time_in_force: str,
    reduce_only: bool,
    guards: OkxRuntimeGuards,
) -> None:
    if order_type not in guards.allowed_order_types:
        raise ValueError(f"OKX order_type {order_type} is not allowed")
    if time_in_force not in guards.allowed_time_in_force:
        raise ValueError(f"OKX time_in_force {time_in_force} is not allowed")
    if order_type == "MARKET" and time_in_force != "IOC":
        raise ValueError("OKX MARKET orders must use IOC semantics")
    if reduce_only and not guards.reduce_only_supported:
        raise ValueError("OKX reduce_only is not supported")
