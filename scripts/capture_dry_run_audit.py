from __future__ import annotations

import argparse
import json
from pathlib import Path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Capture a normalized dry-run audit record."
    )
    parser.add_argument("--operator", required=True)
    parser.add_argument("--stage", required=True)
    parser.add_argument("--venue", required=True, choices=("BYBIT", "BINANCE", "OKX"))
    parser.add_argument("--instrument-id", required=True)
    parser.add_argument("--action", required=True)
    parser.add_argument("--result", required=True, choices=("success", "failure", "skipped"))
    parser.add_argument("--evidence-path", required=True)
    parser.add_argument("--output")
    return parser


def build_record(args: argparse.Namespace) -> dict[str, str]:
    return {
        "operator": args.operator,
        "stage": args.stage,
        "venue": args.venue,
        "instrument_id": args.instrument_id.strip().upper(),
        "action": args.action,
        "result": args.result,
        "evidence_path": args.evidence_path,
    }


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    record = build_record(args)
    payload = json.dumps(record, indent=2, sort_keys=False)

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(payload + "\n", encoding="utf-8")

    print(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
