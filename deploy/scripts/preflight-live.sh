#!/usr/bin/env sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
PROJECT_ROOT=$(CDPATH= cd -- "$SCRIPT_DIR/../.." && pwd)
ENV_FILE="${1:-$PROJECT_ROOT/deploy/.env}"

python "$PROJECT_ROOT/scripts/live_canary_preflight.py" --env-file "$ENV_FILE"
