from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class BybitRecoveryPhase(StrEnum):
    DISCONNECTED = "DISCONNECTED"
    RECONNECTING = "RECONNECTING"
    PRIVATE_STREAM_RESTORED = "PRIVATE_STREAM_RESTORED"
    RESUBSCRIBED = "RESUBSCRIBED"
    RECONCILIATION_PENDING = "RECONCILIATION_PENDING"


class BybitRecoveryEvent(StrEnum):
    RECONNECT_STARTED = "RECONNECT_STARTED"
    PRIVATE_STREAM_READY = "PRIVATE_STREAM_READY"
    RESUBSCRIBE_COMPLETED = "RESUBSCRIBE_COMPLETED"


@dataclass(frozen=True)
class BybitRecoveryState:
    phase: BybitRecoveryPhase
    trade_mode: str
    subscriptions_restored: bool
    reconciliation_required: bool


def begin_bybit_recovery() -> BybitRecoveryState:
    return BybitRecoveryState(
        phase=BybitRecoveryPhase.RECONNECTING,
        trade_mode="REDUCE_ONLY",
        subscriptions_restored=False,
        reconciliation_required=False,
    )


def advance_bybit_recovery(
    state: BybitRecoveryState,
    event: BybitRecoveryEvent,
) -> BybitRecoveryState:
    if state.phase == BybitRecoveryPhase.RECONNECTING:
        if event != BybitRecoveryEvent.PRIVATE_STREAM_READY:
            raise ValueError(
                "Bybit recovery requires PRIVATE_STREAM_READY before resubscribe"
            )
        return BybitRecoveryState(
            phase=BybitRecoveryPhase.PRIVATE_STREAM_RESTORED,
            trade_mode="REDUCE_ONLY",
            subscriptions_restored=False,
            reconciliation_required=False,
        )

    if state.phase == BybitRecoveryPhase.PRIVATE_STREAM_RESTORED:
        if event != BybitRecoveryEvent.RESUBSCRIBE_COMPLETED:
            raise ValueError(
                "Bybit recovery requires RESUBSCRIBE_COMPLETED after private stream restore"
            )
        return BybitRecoveryState(
            phase=BybitRecoveryPhase.RECONCILIATION_PENDING,
            trade_mode="REDUCE_ONLY",
            subscriptions_restored=True,
            reconciliation_required=True,
        )

    raise ValueError(f"Bybit recovery phase {state.phase} does not accept event {event}")
