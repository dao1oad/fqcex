from __future__ import annotations

from perp_platform.control_plane.actions import InMemoryOperatorActionAuditHook
from perp_platform.control_plane.app import ControlPlaneApp


def request_payload(action_type: str, target_scope: dict) -> dict:
    return {
        "action_type": action_type,
        "target_scope": target_scope,
        "requested_by": "alice",
        "reason": "manual intervention",
        "requested_at": "2026-03-21T08:00:00Z",
    }


def test_force_reduce_only_returns_success() -> None:
    audit_hook = InMemoryOperatorActionAuditHook()
    app = ControlPlaneApp(audit_hook=audit_hook)

    response = app.handle(
        "POST",
        "/control-plane/v1/operator-actions/force_reduce_only",
        request_payload("force_reduce_only", {"venue": "BYBIT"}),
    )

    assert response.status_code == 200
    assert response.body["data"]["action_type"] == "force_reduce_only"
    assert response.body["data"]["audit_event_id"] == "audit-1"


def test_force_block_returns_success() -> None:
    app = ControlPlaneApp(audit_hook=InMemoryOperatorActionAuditHook())

    response = app.handle(
        "POST",
        "/control-plane/v1/operator-actions/force_block",
        request_payload("force_block", {"instrument_id": "BTC-USDT-PERP"}),
    )

    assert response.status_code == 200
    assert response.body["data"]["action_type"] == "force_block"


def test_force_resume_requires_completed_recovery_and_reconciliation() -> None:
    app = ControlPlaneApp(audit_hook=InMemoryOperatorActionAuditHook())
    payload = request_payload("force_resume", {"venue": "BYBIT"})
    payload["preconditions"] = {
        "recovery_completed": True,
        "reconciliation_passed": False,
        "has_critical_diffs": False,
    }

    response = app.handle(
        "POST",
        "/control-plane/v1/operator-actions/force_resume",
        payload,
    )

    assert response.status_code == 409
    assert response.body["errors"][0]["code"] == "conflict"


def test_force_resume_succeeds_when_preconditions_are_met() -> None:
    app = ControlPlaneApp(audit_hook=InMemoryOperatorActionAuditHook())
    payload = request_payload("force_resume", {"venue": "BYBIT"})
    payload["preconditions"] = {
        "recovery_completed": True,
        "reconciliation_passed": True,
        "has_critical_diffs": False,
    }

    response = app.handle(
        "POST",
        "/control-plane/v1/operator-actions/force_resume",
        payload,
    )

    assert response.status_code == 200
    assert response.body["data"]["action_type"] == "force_resume"


def test_action_type_must_match_path() -> None:
    app = ControlPlaneApp(audit_hook=InMemoryOperatorActionAuditHook())

    response = app.handle(
        "POST",
        "/control-plane/v1/operator-actions/force_block",
        request_payload("force_reduce_only", {"venue": "BYBIT"}),
    )

    assert response.status_code == 400
    assert response.body["errors"][0]["code"] == "invalid_request"
