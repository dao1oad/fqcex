from __future__ import annotations

import argparse
import json
from pathlib import Path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Build a normalized WebSocket disconnect fault-injection plan."
    )
    parser.add_argument("--venue", required=True, choices=("BYBIT", "BINANCE", "OKX"))
    parser.add_argument("--stream", required=True, choices=("public", "private", "all"))
    parser.add_argument("--duration-seconds", required=True, type=int)
    parser.add_argument("--instrument-id")
    parser.add_argument("--reason", default="manual_fault_injection")
    parser.add_argument("--output")
    return parser


def build_plan(args: argparse.Namespace) -> dict[str, object]:
    if args.duration_seconds <= 0:
        raise ValueError("duration_seconds must be greater than 0")

    instrument_id = None
    if args.instrument_id:
        instrument_id = args.instrument_id.strip().upper()

    return {
        "injector": "ws_disconnect",
        "venue": args.venue,
        "stream": args.stream,
        "duration_seconds": args.duration_seconds,
        "instrument_id": instrument_id,
        "reason": args.reason,
        "action": "disconnect_websocket",
    }


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        plan = build_plan(args)
    except ValueError as exc:
        parser.exit(2, f"{exc}\n")

    payload = json.dumps(plan, indent=2, sort_keys=False)

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(payload + "\n", encoding="utf-8")

    print(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
