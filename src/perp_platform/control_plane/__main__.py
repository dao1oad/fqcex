from __future__ import annotations

import argparse

from .server import serve_control_plane


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="perp_platform.control_plane")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", default=8080, type=int)
    args = parser.parse_args(argv)
    serve_control_plane(host=args.host, port=args.port)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
