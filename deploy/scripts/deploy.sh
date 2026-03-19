#!/usr/bin/env sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
PROJECT_ROOT=$(CDPATH= cd -- "$SCRIPT_DIR/../.." && pwd)
ENV_FILE="$PROJECT_ROOT/deploy/.env"
COMPOSE_FILE="$PROJECT_ROOT/deploy/docker-compose.yml"

"$SCRIPT_DIR/bootstrap-server.sh"

echo "building ${PERP_PLATFORM_IMAGE_REPO:-perp-platform}:${PERP_PLATFORM_IMAGE_TAG:-latest}"
docker compose --env-file "$ENV_FILE" -f "$COMPOSE_FILE" build

echo "running perp-platform bootstrap container"
docker compose --env-file "$ENV_FILE" -f "$COMPOSE_FILE" run --rm perp-platform
