from __future__ import annotations

import argparse
import sys
from pathlib import Path


SUPPORTED_VENUES = ("BYBIT", "BINANCE", "OKX")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate live canary deploy prerequisites."
    )
    parser.add_argument("--env-file", required=True)
    return parser


def parse_env_file(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        key, separator, value = line.partition("=")
        if not separator:
            continue
        values[key.strip()] = value.strip()
    return values


def parse_csv(value: str) -> tuple[str, ...]:
    return tuple(item.strip() for item in value.split(",") if item.strip())


def credentials_field_for_venue(venue: str) -> str:
    return f"{venue}_CREDENTIALS_FILE"


def validate_env(env_path: Path) -> tuple[str, ...]:
    if not env_path.exists():
        return (f"missing env file: {env_path}",)

    env = parse_env_file(env_path)
    errors: list[str] = []

    if env.get("PERP_PLATFORM_ENVIRONMENT") != "live-canary":
        errors.append("PERP_PLATFORM_ENVIRONMENT must be live-canary")

    if env.get("LIVE_CANARY_ENABLED", "").lower() != "true":
        errors.append("LIVE_CANARY_ENABLED must be true")

    venues = parse_csv(env.get("LIVE_CANARY_ALLOWED_VENUES", ""))
    if not venues:
        errors.append("missing live canary venue allowlist")
    else:
        unsupported = sorted(set(venues) - set(SUPPORTED_VENUES))
        if unsupported:
            errors.append(
                "unsupported live canary venues: " + ", ".join(unsupported)
            )

    instruments = parse_csv(env.get("LIVE_CANARY_ALLOWED_INSTRUMENTS", ""))
    if not instruments:
        errors.append("missing live canary instrument allowlist")

    kill_switch_path = env.get("LIVE_CANARY_KILL_SWITCH_PATH", "").strip()
    if not kill_switch_path:
        errors.append("missing kill switch file path")
    elif not Path(kill_switch_path).exists():
        errors.append(f"missing kill switch file: {kill_switch_path}")

    for venue in venues:
        field = credentials_field_for_venue(venue)
        credentials_path = env.get(field, "").strip()
        if not credentials_path:
            errors.append(f"missing credentials file path for {venue}")
            continue
        if not Path(credentials_path).exists():
            errors.append(f"missing credentials file for {venue}: {credentials_path}")

    return tuple(errors)


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    env_path = Path(args.env_file)
    errors = validate_env(env_path)
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print(f"live canary preflight passed: {env_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
