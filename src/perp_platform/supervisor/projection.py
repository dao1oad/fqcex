"""Supervisor tradeability projection helpers for Phase 1."""

from __future__ import annotations

from dataclasses import dataclass

from perp_platform.domain.instruments import InstrumentId, Venue

from .state_machine import SupervisorState


@dataclass(frozen=True, slots=True)
class VenueTradeabilityProjection:
    """Venue-level tradeability projection."""

    venue: Venue
    state: SupervisorState
    allow_open: bool
    allow_reduce: bool
    reason: str


@dataclass(frozen=True, slots=True)
class InstrumentTradeabilityProjection:
    """Instrument-level tradeability projection."""

    venue: Venue
    instrument_id: InstrumentId
    effective_state: SupervisorState
    allow_open: bool
    allow_reduce: bool
    reason: str


_STATE_STRICTNESS: dict[SupervisorState, int] = {
    SupervisorState.LIVE: 0,
    SupervisorState.DEGRADED: 1,
    SupervisorState.RESYNCING: 2,
    SupervisorState.REDUCE_ONLY: 3,
    SupervisorState.BLOCKED: 4,
}


def _state_permissions(state: SupervisorState) -> tuple[bool, bool]:
    if state in (SupervisorState.LIVE, SupervisorState.DEGRADED):
        return True, True

    if state in (SupervisorState.RESYNCING, SupervisorState.REDUCE_ONLY):
        return False, True

    return False, False


def _stricter_state(
    left: SupervisorState,
    right: SupervisorState,
) -> SupervisorState:
    if _STATE_STRICTNESS[left] >= _STATE_STRICTNESS[right]:
        return left
    return right


def project_venue_tradeability(
    venue: Venue,
    state: SupervisorState,
    reason: str,
) -> VenueTradeabilityProjection:
    """Project venue state into venue-level tradeability flags."""

    allow_open, allow_reduce = _state_permissions(state)
    return VenueTradeabilityProjection(
        venue=venue,
        state=state,
        allow_open=allow_open,
        allow_reduce=allow_reduce,
        reason=reason,
    )


def project_instrument_tradeability(
    venue_projection: VenueTradeabilityProjection,
    instrument_id: InstrumentId,
    instrument_state: SupervisorState | None = None,
    reason: str | None = None,
) -> InstrumentTradeabilityProjection:
    """Project instrument-level tradeability without relaxing venue restrictions."""

    if instrument_state is None:
        effective_state = venue_projection.state
        effective_reason = venue_projection.reason
    else:
        effective_state = _stricter_state(venue_projection.state, instrument_state)
        effective_reason = reason if reason is not None else venue_projection.reason

    allow_open, allow_reduce = _state_permissions(effective_state)
    return InstrumentTradeabilityProjection(
        venue=venue_projection.venue,
        instrument_id=instrument_id,
        effective_state=effective_state,
        allow_open=allow_open,
        allow_reduce=allow_reduce,
        reason=effective_reason,
    )
