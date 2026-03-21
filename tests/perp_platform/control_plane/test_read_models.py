from __future__ import annotations

from decimal import Decimal

from perp_platform.checker.signals import CheckerSupervisorSignal
from perp_platform.control_plane.app import ControlPlaneApp
from perp_platform.control_plane.queries import (
    CheckerSignalView,
    InMemoryControlPlaneQueryBackend,
    InstrumentTradeabilityView,
    RecoveryRunView,
    VenueTradeabilityView,
)
from perp_platform.domain import InstrumentId, Venue
from perp_platform.supervisor import SupervisorState


def build_backend() -> InMemoryControlPlaneQueryBackend:
    return InMemoryControlPlaneQueryBackend(
        venues=(
            VenueTradeabilityView(
                venue="BYBIT",
                supervisor_state="LIVE",
                allow_open=True,
                allow_reduce=True,
                reason="healthy",
            ),
        ),
        instruments=(
            InstrumentTradeabilityView(
                instrument_id="BTC-USDT-PERP",
                venue="BYBIT",
                supervisor_state="LIVE",
                allow_open=True,
                allow_reduce=True,
                reason="healthy",
            ),
        ),
        recovery_runs=(
            RecoveryRunView(
                run_id="recovery-1",
                phase="RECONCILIATION_PENDING",
                status="running",
                trigger_reason="private_stream_restored",
                blockers_json="[]",
            ),
        ),
        checker_signals=(
            CheckerSignalView(
                signal_id="checker-1",
                venue="BYBIT",
                instrument_id="BTC-USDT-PERP",
                suggested_state="LIVE",
                reason="checker_healthy",
                stale=False,
                diverged=False,
                age_seconds=0.5,
                max_divergence_bps="0",
            ),
        ),
    )


def test_venues_list_returns_items_envelope() -> None:
    app = ControlPlaneApp(query_backend=build_backend())

    response = app.handle("GET", "/control-plane/v1/venues")

    assert response.status_code == 200
    assert response.body["data"]["items"] == [
        {
            "venue": "BYBIT",
            "supervisor_state": "LIVE",
            "allow_open": True,
            "allow_reduce": True,
            "reason": "healthy",
        }
    ]


def test_venue_detail_returns_single_resource() -> None:
    app = ControlPlaneApp(query_backend=build_backend())

    response = app.handle("GET", "/control-plane/v1/venues/BYBIT")

    assert response.status_code == 200
    assert response.body["data"]["venue"] == "BYBIT"
    assert response.body["data"]["supervisor_state"] == "LIVE"


def test_instrument_detail_returns_single_resource() -> None:
    app = ControlPlaneApp(query_backend=build_backend())

    response = app.handle("GET", "/control-plane/v1/instruments/BTC-USDT-PERP")

    assert response.status_code == 200
    assert response.body["data"]["instrument_id"] == "BTC-USDT-PERP"
    assert response.body["data"]["venue"] == "BYBIT"


def test_recovery_runs_list_returns_items_envelope() -> None:
    app = ControlPlaneApp(query_backend=build_backend())

    response = app.handle("GET", "/control-plane/v1/recovery/runs")

    assert response.status_code == 200
    assert response.body["data"]["items"] == [
        {
            "run_id": "recovery-1",
            "phase": "RECONCILIATION_PENDING",
            "status": "running",
            "trigger_reason": "private_stream_restored",
            "blockers_json": "[]",
        }
    ]


def test_checker_signal_detail_returns_single_resource() -> None:
    app = ControlPlaneApp(query_backend=build_backend())

    response = app.handle("GET", "/control-plane/v1/checker/signals/checker-1")

    assert response.status_code == 200
    assert response.body["data"]["signal_id"] == "checker-1"
    assert response.body["data"]["suggested_state"] == "LIVE"


def test_missing_resource_returns_not_found() -> None:
    app = ControlPlaneApp(query_backend=build_backend())

    response = app.handle("GET", "/control-plane/v1/venues/OKX")

    assert response.status_code == 404
    assert response.body["errors"][0]["code"] == "not_found"
