from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import uuid4


@dataclass(frozen=True)
class ControlPlaneResponse:
    status_code: int
    body: dict


class ControlPlaneApp:
    """Minimal control-plane request dispatcher."""

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

    def _meta(self) -> dict:
        return {
            "request_id": uuid4().hex,
            "generated_at": datetime.now(timezone.utc)
            .isoformat()
            .replace("+00:00", "Z"),
        }
