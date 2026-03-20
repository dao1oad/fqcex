from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

INITIAL_BACKOFF_SECONDS = 5
BACKOFF_MULTIPLIER = 2
MAX_BACKOFF_SECONDS = 60


class BinanceRecoveryPhase(StrEnum):
    BACKING_OFF = "BACKING_OFF"
    RECONNECTING = "RECONNECTING"
    PRIVATE_STREAM_RESTORED = "PRIVATE_STREAM_RESTORED"
    RECONCILIATION_PENDING = "RECONCILIATION_PENDING"


class BinanceRecoveryEvent(StrEnum):
    BACKOFF_ELAPSED = "BACKOFF_ELAPSED"
    PRIVATE_STREAM_READY = "PRIVATE_STREAM_READY"
    RESUBSCRIBE_COMPLETED = "RESUBSCRIBE_COMPLETED"
    RATE_LIMIT_HIT = "RATE_LIMIT_HIT"


@dataclass(frozen=True)
class BinanceRecoveryState:
    phase: BinanceRecoveryPhase
    trade_mode: str
    attempt: int
    backoff_seconds: int
    subscriptions_restored: bool
    reconciliation_required: bool


def begin_binance_recovery() -> BinanceRecoveryState:
    return BinanceRecoveryState(
        phase=BinanceRecoveryPhase.BACKING_OFF,
        trade_mode="REDUCE_ONLY",
        attempt=1,
        backoff_seconds=INITIAL_BACKOFF_SECONDS,
        subscriptions_restored=False,
        reconciliation_required=False,
    )


def advance_binance_recovery(
    state: BinanceRecoveryState,
    event: BinanceRecoveryEvent,
) -> BinanceRecoveryState:
    if event == BinanceRecoveryEvent.RATE_LIMIT_HIT:
        next_backoff = min(state.backoff_seconds * BACKOFF_MULTIPLIER, MAX_BACKOFF_SECONDS)
        return BinanceRecoveryState(
            phase=BinanceRecoveryPhase.BACKING_OFF,
            trade_mode="REDUCE_ONLY",
            attempt=state.attempt + 1,
            backoff_seconds=next_backoff,
            subscriptions_restored=False,
            reconciliation_required=False,
        )

    if state.phase == BinanceRecoveryPhase.BACKING_OFF:
        if event != BinanceRecoveryEvent.BACKOFF_ELAPSED:
            raise ValueError(
                "Binance recovery requires BACKOFF_ELAPSED before reconnecting"
            )
        return BinanceRecoveryState(
            phase=BinanceRecoveryPhase.RECONNECTING,
            trade_mode="REDUCE_ONLY",
            attempt=state.attempt,
            backoff_seconds=state.backoff_seconds,
            subscriptions_restored=False,
            reconciliation_required=False,
        )

    if state.phase == BinanceRecoveryPhase.RECONNECTING:
        if event != BinanceRecoveryEvent.PRIVATE_STREAM_READY:
            raise ValueError(
                "Binance recovery requires PRIVATE_STREAM_READY after reconnecting"
            )
        return BinanceRecoveryState(
            phase=BinanceRecoveryPhase.PRIVATE_STREAM_RESTORED,
            trade_mode="REDUCE_ONLY",
            attempt=state.attempt,
            backoff_seconds=state.backoff_seconds,
            subscriptions_restored=False,
            reconciliation_required=False,
        )

    if state.phase == BinanceRecoveryPhase.PRIVATE_STREAM_RESTORED:
        if event != BinanceRecoveryEvent.RESUBSCRIBE_COMPLETED:
            raise ValueError(
                "Binance recovery requires RESUBSCRIBE_COMPLETED after private stream restore"
            )
        return BinanceRecoveryState(
            phase=BinanceRecoveryPhase.RECONCILIATION_PENDING,
            trade_mode="REDUCE_ONLY",
            attempt=state.attempt,
            backoff_seconds=state.backoff_seconds,
            subscriptions_restored=True,
            reconciliation_required=True,
        )

    raise ValueError(
        f"Binance recovery phase {state.phase} does not accept event {event}"
    )
