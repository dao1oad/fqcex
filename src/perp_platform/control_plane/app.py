from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import uuid4

from .actions import (
    ForceResumePreconditions,
    InMemoryOperatorActionAuditHook,
    OperatorActionRequest,
    OperatorActionResult,
)
from .queries import (
    ControlPlaneQueryBackend,
    InMemoryControlPlaneQueryBackend,
    serialize_item,
    serialize_items,
)


@dataclass(frozen=True)
class ControlPlaneResponse:
    status_code: int
    body: dict


class ControlPlaneApp:
    """Minimal control-plane request dispatcher."""

    def __init__(
        self,
        query_backend: ControlPlaneQueryBackend | None = None,
        audit_hook: InMemoryOperatorActionAuditHook | None = None,
    ) -> None:
        self._query_backend = query_backend or InMemoryControlPlaneQueryBackend()
        self._audit_hook = audit_hook or InMemoryOperatorActionAuditHook()

    def handle(
        self,
        method: str,
        path: str,
        payload: dict | None = None,
    ) -> ControlPlaneResponse:
        if method == "POST":
            return self._handle_post(path, payload)

        if method != "GET":
            return self._invalid_request("control plane method not allowed")

        if path == "/control-plane/v1/health":
            return self._success({"service": "control-plane", "status": "ok"})

        if path == "/control-plane/v1/readiness":
            return self._success({"service": "control-plane", "status": "ready"})

        if path == "/control-plane/v1/venues":
            return self._success({"items": serialize_items(self._query_backend.list_venues())})

        if path.startswith("/control-plane/v1/venues/"):
            venue = path.removeprefix("/control-plane/v1/venues/")
            item = self._query_backend.get_venue(venue)
            if item is None:
                return self._not_found()
            return self._success(serialize_item(item))

        if path == "/control-plane/v1/instruments":
            return self._success(
                {"items": serialize_items(self._query_backend.list_instruments())}
            )

        if path.startswith("/control-plane/v1/instruments/"):
            instrument_id = path.removeprefix("/control-plane/v1/instruments/")
            item = self._query_backend.get_instrument(instrument_id)
            if item is None:
                return self._not_found()
            return self._success(serialize_item(item))

        if path == "/control-plane/v1/recovery/runs":
            return self._success(
                {"items": serialize_items(self._query_backend.list_recovery_runs())}
            )

        if path.startswith("/control-plane/v1/recovery/runs/"):
            run_id = path.removeprefix("/control-plane/v1/recovery/runs/")
            item = self._query_backend.get_recovery_run(run_id)
            if item is None:
                return self._not_found()
            return self._success(serialize_item(item))

        if path == "/control-plane/v1/checker/signals":
            return self._success(
                {"items": serialize_items(self._query_backend.list_checker_signals())}
            )

        if path.startswith("/control-plane/v1/checker/signals/"):
            signal_id = path.removeprefix("/control-plane/v1/checker/signals/")
            item = self._query_backend.get_checker_signal(signal_id)
            if item is None:
                return self._not_found()
            return self._success(serialize_item(item))

        return self._not_found()

    def _handle_post(self, path: str, payload: dict | None) -> ControlPlaneResponse:
        if path.startswith("/control-plane/v1/operator-actions/"):
            action_name = path.removeprefix("/control-plane/v1/operator-actions/")
            return self._handle_operator_action(action_name, payload)

        return self._invalid_request("control plane method not allowed")

    def _handle_operator_action(
        self,
        action_name: str,
        payload: dict | None,
    ) -> ControlPlaneResponse:
        if payload is None:
            return self._invalid_request("control plane request body is required")

        for field in ("action_type", "target_scope", "requested_by", "reason", "requested_at"):
            if field not in payload:
                return self._invalid_request(f"missing required field: {field}")

        if payload["action_type"] != action_name:
            return self._invalid_request("action_type does not match request path")

        preconditions = None
        if payload.get("preconditions") is not None:
            preconditions = ForceResumePreconditions(**payload["preconditions"])

        request = OperatorActionRequest(
            action_type=payload["action_type"],
            target_scope=payload["target_scope"],
            requested_by=payload["requested_by"],
            reason=payload["reason"],
            requested_at=payload["requested_at"],
            preconditions=preconditions,
        )

        if request.action_type == "force_resume":
            if request.preconditions is None:
                return self._conflict(
                    "force_resume requires satisfied recovery and reconciliation preconditions"
                )
            if (
                not request.preconditions.recovery_completed
                or not request.preconditions.reconciliation_passed
                or request.preconditions.has_critical_diffs
            ):
                return self._conflict(
                    "force_resume requires completed recovery, passed reconciliation, and no critical diffs"
                )

        audit_event_id = self._audit_hook.record(request)
        result = OperatorActionResult(
            action_type=request.action_type,
            target_scope=request.target_scope,
            requested_by=request.requested_by,
            requested_at=request.requested_at,
            audit_event_id=audit_event_id,
        )
        return self._success(serialize_item(result))

    def _success(self, data: dict) -> ControlPlaneResponse:
        return ControlPlaneResponse(
            status_code=200,
            body={
                "data": data,
                "meta": self._meta(),
                "errors": [],
            },
        )

    def _error(self, status_code: int, code: str, message: str) -> ControlPlaneResponse:
        return ControlPlaneResponse(
            status_code=status_code,
            body={
                "data": None,
                "meta": self._meta(),
                "errors": [
                    {
                        "code": code,
                        "message": message,
                    }
                ],
            },
        )

    def _not_found(self) -> ControlPlaneResponse:
        return self._error(
            status_code=404,
            code="not_found",
            message="control plane resource not found",
        )

    def _invalid_request(self, message: str) -> ControlPlaneResponse:
        return self._error(
            status_code=400,
            code="invalid_request",
            message=message,
        )

    def _conflict(self, message: str) -> ControlPlaneResponse:
        return self._error(
            status_code=409,
            code="conflict",
            message=message,
        )

    def _meta(self) -> dict:
        return {
            "request_id": uuid4().hex,
            "generated_at": datetime.now(timezone.utc)
            .isoformat()
            .replace("+00:00", "Z"),
        }
