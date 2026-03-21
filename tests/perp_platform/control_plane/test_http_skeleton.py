import json
import threading
from contextlib import closing
from urllib.error import HTTPError
from urllib.request import urlopen

import pytest

from perp_platform.control_plane.app import ControlPlaneApp
from perp_platform.control_plane.server import create_control_plane_server


def test_health_endpoint_returns_success_envelope() -> None:
    app = ControlPlaneApp()

    response = app.handle("GET", "/control-plane/v1/health")

    assert response.status_code == 200
    assert response.body["data"] == {"service": "control-plane", "status": "ok"}
    assert response.body["errors"] == []
    assert response.body["meta"]["request_id"]
    assert response.body["meta"]["generated_at"]


def test_readiness_endpoint_returns_success_envelope() -> None:
    app = ControlPlaneApp()

    response = app.handle("GET", "/control-plane/v1/readiness")

    assert response.status_code == 200
    assert response.body["data"] == {"service": "control-plane", "status": "ready"}
    assert response.body["errors"] == []
    assert response.body["meta"]["request_id"]
    assert response.body["meta"]["generated_at"]


def test_unknown_path_returns_not_found_envelope() -> None:
    app = ControlPlaneApp()

    response = app.handle("GET", "/control-plane/v1/unknown")

    assert response.status_code == 404
    assert response.body["data"] is None
    assert response.body["errors"] == [
        {
            "code": "not_found",
            "message": "control plane resource not found",
        }
    ]


def test_http_server_serves_health_endpoint() -> None:
    with closing(create_control_plane_server(host="127.0.0.1", port=0)) as server:
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()

        url = f"http://127.0.0.1:{server.server_port}/control-plane/v1/health"
        with urlopen(url) as response:
            payload = json.loads(response.read().decode("utf-8"))

        server.shutdown()
        thread.join(timeout=2)

    assert payload["data"] == {"service": "control-plane", "status": "ok"}
    assert payload["errors"] == []
    assert payload["meta"]["request_id"]


def test_http_server_returns_404_envelope() -> None:
    with closing(create_control_plane_server(host="127.0.0.1", port=0)) as server:
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()

        url = f"http://127.0.0.1:{server.server_port}/control-plane/v1/unknown"
        with pytest.raises(HTTPError) as exc_info:
            urlopen(url)

        payload = json.loads(exc_info.value.read().decode("utf-8"))

        server.shutdown()
        thread.join(timeout=2)

    assert exc_info.value.code == 404
    assert payload["errors"][0]["code"] == "not_found"
