from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from ..domain import Venue
from ..supervisor import SupervisorState
from .policies import CheckerPolicyResult

CHECKER_HEALTHY_REASON = "checker_healthy"
CHECKER_STALE_REASON = "checker_stale"
CHECKER_TOP_OF_BOOK_DIVERGED_REASON = "checker_top_of_book_diverged"


@dataclass(frozen=True)
class CheckerSupervisorSignal:
    venue: Venue
    instrument_id: str
    suggested_state: SupervisorState
    reason: str
    stale: bool
    diverged: bool
    age_seconds: float
    max_divergence_bps: Decimal


def build_checker_supervisor_signal(
    policy_result: CheckerPolicyResult,
) -> CheckerSupervisorSignal:
    if policy_result.diverged:
        suggested_state = SupervisorState.RESYNCING
        reason = CHECKER_TOP_OF_BOOK_DIVERGED_REASON
    elif policy_result.stale:
        suggested_state = SupervisorState.DEGRADED
        reason = CHECKER_STALE_REASON
    else:
        suggested_state = SupervisorState.LIVE
        reason = CHECKER_HEALTHY_REASON

    return CheckerSupervisorSignal(
        venue=policy_result.venue,
        instrument_id=policy_result.instrument_id,
        suggested_state=suggested_state,
        reason=reason,
        stale=policy_result.stale,
        diverged=policy_result.diverged,
        age_seconds=policy_result.age_seconds,
        max_divergence_bps=policy_result.max_divergence_bps,
    )
