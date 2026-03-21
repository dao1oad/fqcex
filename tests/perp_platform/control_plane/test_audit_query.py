from __future__ import annotations

from perp_platform.control_plane.app import ControlPlaneApp
from perp_platform.control_plane.queries import (
    AuditEventView,
    InMemoryControlPlaneQueryBackend,
)


def build_backend() -> InMemoryControlPlaneQueryBackend:
    return InMemoryControlPlaneQueryBackend(
        audit_events=(
            AuditEventView(
                event_id="audit-1",
                event_type="operator_action",
                occurred_at="2026-03-21T08:00:00Z",
                source_component="control-plane",
                scope={"venue": "BYBIT"},
                correlation_id="corr-1",
                recorded_by="alice",
            ),
            AuditEventView(
                event_id="audit-2",
                event_type="recovery",
                occurred_at="2026-03-21T09:00:00Z",
                source_component="supervisor",
                scope={"venue": "OKX"},
                correlation_id="corr-2",
                recorded_by="system",
            ),
        )
    )


def test_audit_events_list_returns_items() -> None:
    app = ControlPlaneApp(query_backend=build_backend())

    response = app.handle("GET", "/control-plane/v1/audit/events")

    assert response.status_code == 200
    assert len(response.body["data"]["items"]) == 2


def test_audit_event_detail_returns_single_resource() -> None:
    app = ControlPlaneApp(query_backend=build_backend())

    response = app.handle("GET", "/control-plane/v1/audit/events/audit-1")

    assert response.status_code == 200
    assert response.body["data"]["event_id"] == "audit-1"
    assert response.body["data"]["correlation_id"] == "corr-1"


def test_audit_events_can_filter_by_correlation_id() -> None:
    app = ControlPlaneApp(query_backend=build_backend())

    response = app.handle("GET", "/control-plane/v1/audit/events?correlation_id=corr-2")

    assert response.status_code == 200
    assert response.body["data"]["items"] == [
        {
            "event_id": "audit-2",
            "event_type": "recovery",
            "occurred_at": "2026-03-21T09:00:00Z",
            "source_component": "supervisor",
            "scope": {"venue": "OKX"},
            "correlation_id": "corr-2",
            "recorded_by": "system",
        }
    ]


def test_audit_events_can_filter_by_time_window() -> None:
    app = ControlPlaneApp(query_backend=build_backend())

    response = app.handle(
        "GET",
        "/control-plane/v1/audit/events?occurred_after=2026-03-21T08:30:00Z&occurred_before=2026-03-21T09:30:00Z",
    )

    assert response.status_code == 200
    assert [item["event_id"] for item in response.body["data"]["items"]] == ["audit-2"]


def test_missing_audit_event_returns_not_found() -> None:
    app = ControlPlaneApp(query_backend=build_backend())

    response = app.handle("GET", "/control-plane/v1/audit/events/audit-999")

    assert response.status_code == 404
    assert response.body["errors"][0]["code"] == "not_found"
