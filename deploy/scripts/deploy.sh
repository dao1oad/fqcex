#!/usr/bin/env sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
PROJECT_ROOT=$(CDPATH= cd -- "$SCRIPT_DIR/../.." && pwd)
ENV_FILE="${1:-$PROJECT_ROOT/deploy/.env}"
COMPOSE_FILE="$PROJECT_ROOT/deploy/docker-compose.yml"

"$SCRIPT_DIR/bootstrap-server.sh" "$ENV_FILE"

if docker compose version >/dev/null 2>&1; then
  DOCKER_COMPOSE_BIN="docker compose"
  DOCKER_COMPOSE_FLAVOR="plugin"
elif command -v docker-compose >/dev/null 2>&1 && docker-compose version >/dev/null 2>&1; then
  DOCKER_COMPOSE_BIN="docker-compose"
  DOCKER_COMPOSE_FLAVOR="standalone"
else
  echo "docker compose or docker-compose is required but is not available" >&2
  exit 1
fi

echo "building ${PERP_PLATFORM_IMAGE_REPO:-perp-platform}:${PERP_PLATFORM_IMAGE_TAG:-latest}"
LIVE_CANARY_ENV_FILE="$ENV_FILE" sh -c "$DOCKER_COMPOSE_BIN --env-file \"$ENV_FILE\" -f \"$COMPOSE_FILE\" build"

echo "starting live deploy stack"
if [ "$DOCKER_COMPOSE_FLAVOR" = "standalone" ]; then
  LIVE_CANARY_ENV_FILE="$ENV_FILE" sh -c "$DOCKER_COMPOSE_BIN --env-file \"$ENV_FILE\" -f \"$COMPOSE_FILE\" rm -sf control-plane operator-ui || true"
fi
LIVE_CANARY_ENV_FILE="$ENV_FILE" sh -c "$DOCKER_COMPOSE_BIN --env-file \"$ENV_FILE\" -f \"$COMPOSE_FILE\" up -d --force-recreate control-plane operator-ui"

CONTROL_PLANE_PORT=$(awk -F= '/^CONTROL_PLANE_PORT=/{print $2}' "$ENV_FILE")
if [ -z "$CONTROL_PLANE_PORT" ]; then
  CONTROL_PLANE_PORT=8080
fi

OPERATOR_UI_PORT=$(awk -F= '/^OPERATOR_UI_PORT=/{print $2}' "$ENV_FILE")
if [ -z "$OPERATOR_UI_PORT" ]; then
  OPERATOR_UI_PORT=4173
fi

python3 -c "import sys, urllib.request; urllib.request.urlopen('http://127.0.0.1:${CONTROL_PLANE_PORT}/control-plane/v1/health'); urllib.request.urlopen('http://127.0.0.1:${OPERATOR_UI_PORT}/'); print('live deploy stack healthy')"
