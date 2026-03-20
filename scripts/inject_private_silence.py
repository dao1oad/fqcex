from __future__ import annotations

import argparse
import json
from pathlib import Path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Build a normalized private-stream silence fault-injection plan."
    )
    parser.add_argument("--venue", required=True, choices=("BYBIT", "BINANCE", "OKX"))
    parser.add_argument("--duration-seconds", required=True, type=int)
    parser.add_argument("--scope", default="account", choices=("account", "venue"))
    parser.add_argument("--reason", default="manual_fault_injection")
    parser.add_argument("--output")
    return parser


def build_plan(args: argparse.Namespace) -> dict[str, object]:
    if args.duration_seconds <= 0:
        raise ValueError("duration_seconds must be greater than 0")

    return {
        "injector": "private_silence",
        "venue": args.venue,
        "scope": args.scope,
        "duration_seconds": args.duration_seconds,
        "reason": args.reason,
        "action": "silence_private_stream",
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
