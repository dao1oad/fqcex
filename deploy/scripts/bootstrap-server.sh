#!/usr/bin/env sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
PROJECT_ROOT=$(CDPATH= cd -- "$SCRIPT_DIR/../.." && pwd)
ENV_FILE="$PROJECT_ROOT/deploy/.env"
STATE_DIR="$PROJECT_ROOT/deploy/state"

if ! command -v docker >/dev/null 2>&1; then
  echo "docker is required but was not found in PATH" >&2
  exit 1
fi

if ! docker compose version >/dev/null 2>&1; then
  echo "docker compose is required but is not available" >&2
  exit 1
fi

mkdir -p "$STATE_DIR"

if [ ! -f "$ENV_FILE" ]; then
  echo "missing deploy/.env; copy deploy/.env.example to deploy/.env before deploying" >&2
  exit 1
fi

echo "bootstrap checks passed"
