from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import uuid4

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

    def __init__(self, query_backend: ControlPlaneQueryBackend | None = None) -> None:
        self._query_backend = query_backend or InMemoryControlPlaneQueryBackend()

    def handle(self, method: str, path: str) -> ControlPlaneResponse:
        if method != "GET":
            return self._error(
                status_code=405,
                code="invalid_request",
                message="control plane method not allowed",
            )

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

        return self._error(
            status_code=404,
            code="not_found",
            message="control plane resource not found",
        )

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

    def _meta(self) -> dict:
        return {
            "request_id": uuid4().hex,
            "generated_at": datetime.now(timezone.utc)
            .isoformat()
            .replace("+00:00", "Z"),
        }
