from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from .reconciliation import BybitReconciliationResult
from .recovery import BybitRecoveryPhase, BybitRecoveryState


class BybitTradeabilityMode(StrEnum):
    REDUCE_ONLY = "REDUCE_ONLY"
    BLOCKED = "BLOCKED"


@dataclass(frozen=True)
class BybitTradeabilityProjection:
    mode: BybitTradeabilityMode
    reason: str
    blockers: list[str]


def project_bybit_tradeability(
    recovery_state: BybitRecoveryState,
    reconciliation_result: BybitReconciliationResult | None,
) -> BybitTradeabilityProjection:
    if recovery_state.phase != BybitRecoveryPhase.RECONCILIATION_PENDING:
        return BybitTradeabilityProjection(
            mode=BybitTradeabilityMode.REDUCE_ONLY,
            reason="recovery_in_progress",
            blockers=[],
        )

    if reconciliation_result is None:
        return BybitTradeabilityProjection(
            mode=BybitTradeabilityMode.REDUCE_ONLY,
            reason="reconciliation_pending",
            blockers=[],
        )

    if reconciliation_result.passed is False:
        return BybitTradeabilityProjection(
            mode=BybitTradeabilityMode.BLOCKED,
            reason="reconciliation_failed",
            blockers=[
                *reconciliation_result.order_diffs,
                *reconciliation_result.position_diffs,
                *reconciliation_result.balance_diffs,
            ],
        )

    return BybitTradeabilityProjection(
        mode=BybitTradeabilityMode.REDUCE_ONLY,
        reason="cooldown_pending",
        blockers=[],
    )
