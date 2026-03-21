from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from .app import ControlPlaneApp


class ControlPlaneHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:  # noqa: N802
        self._write_response(self.server.app.handle("GET", self.path))

    def do_POST(self) -> None:  # noqa: N802
        content_length = int(self.headers.get("Content-Length", "0"))
        payload = None
        if content_length > 0:
            payload = json.loads(self.rfile.read(content_length).decode("utf-8"))
        self._write_response(self.server.app.handle("POST", self.path, payload))

    def log_message(self, format: str, *args: object) -> None:
        return

    def _write_response(self, response) -> None:
        payload = json.dumps(response.body).encode("utf-8")
        self.send_response(response.status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)


def create_control_plane_server(
    host: str = "127.0.0.1",
    port: int = 8080,
    app: ControlPlaneApp | None = None,
) -> ThreadingHTTPServer:
    server = ThreadingHTTPServer((host, port), ControlPlaneHTTPRequestHandler)
    server.app = app or ControlPlaneApp()
    server.close = server.server_close
    return server


def serve_control_plane(host: str = "127.0.0.1", port: int = 8080) -> None:
    with create_control_plane_server(host=host, port=port) as server:
        server.serve_forever()
