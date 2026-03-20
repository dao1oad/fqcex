from __future__ import annotations

import argparse
import json
from pathlib import Path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Build a normalized reconcile-diff fault-injection plan."
    )
    parser.add_argument("--venue", required=True, choices=("BYBIT", "BINANCE", "OKX"))
    parser.add_argument("--resource", required=True, choices=("order", "position", "balance"))
    parser.add_argument("--diff-kind", required=True, choices=("missing", "extra", "mismatch"))
    parser.add_argument("--instrument-id")
    parser.add_argument("--reason", default="manual_fault_injection")
    parser.add_argument("--output")
    return parser


def build_plan(args: argparse.Namespace) -> dict[str, object]:
    instrument_id = None
    if args.instrument_id:
        instrument_id = args.instrument_id.strip().upper()

    return {
        "injector": "reconcile_diff",
        "venue": args.venue,
        "resource": args.resource,
        "diff_kind": args.diff_kind,
        "instrument_id": instrument_id,
        "reason": args.reason,
        "action": "inject_reconcile_diff",
    }


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    plan = build_plan(args)
    payload = json.dumps(plan, indent=2, sort_keys=False)

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(payload + "\n", encoding="utf-8")

    print(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
