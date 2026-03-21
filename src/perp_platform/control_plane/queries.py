from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Protocol


@dataclass(frozen=True)
class VenueTradeabilityView:
    venue: str
    supervisor_state: str
    allow_open: bool
    allow_reduce: bool
    reason: str


@dataclass(frozen=True)
class InstrumentTradeabilityView:
    instrument_id: str
    venue: str
    supervisor_state: str
    allow_open: bool
    allow_reduce: bool
    reason: str


@dataclass(frozen=True)
class RecoveryRunView:
    run_id: str
    phase: str
    status: str
    trigger_reason: str
    blockers_json: str


@dataclass(frozen=True)
class CheckerSignalView:
    signal_id: str
    venue: str
    instrument_id: str
    suggested_state: str
    reason: str
    stale: bool
    diverged: bool
    age_seconds: float
    max_divergence_bps: str


@dataclass(frozen=True)
class AuditEventView:
    event_id: str
    event_type: str
    occurred_at: str
    source_component: str
    scope: dict
    correlation_id: str
    recorded_by: str


@dataclass(frozen=True)
class AuditEventQuery:
    correlation_id: str | None = None
    occurred_after: datetime | None = None
    occurred_before: datetime | None = None


class ControlPlaneQueryBackend(Protocol):
    def list_venues(self) -> tuple[VenueTradeabilityView, ...]: ...

    def get_venue(self, venue: str) -> VenueTradeabilityView | None: ...

    def list_instruments(self) -> tuple[InstrumentTradeabilityView, ...]: ...

    def get_instrument(self, instrument_id: str) -> InstrumentTradeabilityView | None: ...

    def list_recovery_runs(self) -> tuple[RecoveryRunView, ...]: ...

    def get_recovery_run(self, run_id: str) -> RecoveryRunView | None: ...

    def list_checker_signals(self) -> tuple[CheckerSignalView, ...]: ...

    def get_checker_signal(self, signal_id: str) -> CheckerSignalView | None: ...

    def list_audit_events(self, query: AuditEventQuery) -> tuple[AuditEventView, ...]: ...

    def get_audit_event(self, event_id: str) -> AuditEventView | None: ...


@dataclass(frozen=True)
class InMemoryControlPlaneQueryBackend:
    venues: tuple[VenueTradeabilityView, ...] = ()
    instruments: tuple[InstrumentTradeabilityView, ...] = ()
    recovery_runs: tuple[RecoveryRunView, ...] = ()
    checker_signals: tuple[CheckerSignalView, ...] = ()
    audit_events: tuple[AuditEventView, ...] = ()

    def list_venues(self) -> tuple[VenueTradeabilityView, ...]:
        return self.venues

    def get_venue(self, venue: str) -> VenueTradeabilityView | None:
        return next((item for item in self.venues if item.venue == venue), None)

    def list_instruments(self) -> tuple[InstrumentTradeabilityView, ...]:
        return self.instruments

    def get_instrument(self, instrument_id: str) -> InstrumentTradeabilityView | None:
        return next(
            (item for item in self.instruments if item.instrument_id == instrument_id),
            None,
        )

    def list_recovery_runs(self) -> tuple[RecoveryRunView, ...]:
        return self.recovery_runs

    def get_recovery_run(self, run_id: str) -> RecoveryRunView | None:
        return next((item for item in self.recovery_runs if item.run_id == run_id), None)

    def list_checker_signals(self) -> tuple[CheckerSignalView, ...]:
        return self.checker_signals

    def get_checker_signal(self, signal_id: str) -> CheckerSignalView | None:
        return next(
            (item for item in self.checker_signals if item.signal_id == signal_id),
            None,
        )

    def list_audit_events(self, query: AuditEventQuery) -> tuple[AuditEventView, ...]:
        items = self.audit_events
        if query.correlation_id is not None:
            items = tuple(
                item for item in items if item.correlation_id == query.correlation_id
            )
        if query.occurred_after is not None:
            items = tuple(
                item
                for item in items
                if parse_rfc3339_timestamp(item.occurred_at) >= query.occurred_after
            )
        if query.occurred_before is not None:
            items = tuple(
                item
                for item in items
                if parse_rfc3339_timestamp(item.occurred_at) <= query.occurred_before
            )
        return items

    def get_audit_event(self, event_id: str) -> AuditEventView | None:
        return next((item for item in self.audit_events if item.event_id == event_id), None)


def serialize_items(items: tuple[object, ...]) -> list[dict]:
    return [asdict(item) for item in items]


def serialize_item(item: object) -> dict:
    return asdict(item)


def serialize_audit_items(items: tuple[AuditEventView, ...]) -> list[dict]:
    return [serialize_audit_item(item) for item in items]


def serialize_audit_item(item: AuditEventView) -> dict:
    redacted_scope = {
        key: value
        for key, value in item.scope.items()
        if key in {"venue", "instrument_id", "run_id"}
    }
    return {
        "event_id": item.event_id,
        "event_type": item.event_type,
        "occurred_at": item.occurred_at,
        "source_component": item.source_component,
        "scope": redacted_scope,
        "correlation_id": item.correlation_id,
        "recorded_by": "redacted",
    }


def parse_rfc3339_timestamp(value: str) -> datetime:
    normalized = value.replace("Z", "+00:00")
    parsed = datetime.fromisoformat(normalized)
    if parsed.tzinfo is None:
        raise ValueError("timestamp must include timezone")
    return parsed
