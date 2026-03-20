from __future__ import annotations

from dataclasses import dataclass

from .bootstrap import BybitRuntimeBootstrapResult
from .guards import validate_bybit_order_capability


@dataclass(frozen=True)
class BybitOrderPath:
    rest_base_url: str
    category: str
    settle_coin: str
    order_type: str
    time_in_force: str
    reduce_only: bool
    private_client_required: bool


def build_bybit_order_path(
    order_type: str,
    time_in_force: str,
    reduce_only: bool,
    bootstrap_result: BybitRuntimeBootstrapResult,
) -> BybitOrderPath:
    validate_bybit_order_capability(
        order_type=order_type,
        time_in_force=time_in_force,
        reduce_only=reduce_only,
        guards=bootstrap_result.guards,
    )

    execution_client = bootstrap_result.runtime.execution_client
    return BybitOrderPath(
        rest_base_url=execution_client.rest_base_url,
        category=execution_client.category,
        settle_coin=execution_client.settle_coin,
        order_type=order_type,
        time_in_force=time_in_force,
        reduce_only=reduce_only,
        private_client_required=True,
    )
