from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class BybitRuntimeGuards:
    position_mode: str
    margin_mode: str
    default_leverage: int
    max_leverage: int
    allowed_order_types: tuple[str, ...]
    allowed_time_in_force: tuple[str, ...]
    reduce_only_supported: bool


def build_bybit_runtime_guards() -> BybitRuntimeGuards:
    return BybitRuntimeGuards(
        position_mode="one_way",
        margin_mode="isolated",
        default_leverage=2,
        max_leverage=3,
        allowed_order_types=("LIMIT", "MARKET"),
        allowed_time_in_force=("GTC", "IOC"),
        reduce_only_supported=True,
    )


def validate_bybit_leverage(leverage: int, guards: BybitRuntimeGuards) -> None:
    if leverage < 1:
        raise ValueError("Bybit leverage must be >= 1")
    if leverage > guards.max_leverage:
        raise ValueError(
            f"Bybit leverage {leverage} exceeds max leverage {guards.max_leverage}"
        )


def validate_bybit_order_capability(
    order_type: str,
    time_in_force: str,
    reduce_only: bool,
    guards: BybitRuntimeGuards,
) -> None:
    if order_type not in guards.allowed_order_types:
        raise ValueError(f"Bybit order_type {order_type} is not allowed")
    if time_in_force not in guards.allowed_time_in_force:
        raise ValueError(f"Bybit time_in_force {time_in_force} is not allowed")
    if reduce_only and not guards.reduce_only_supported:
        raise ValueError("Bybit reduce_only is not supported")
