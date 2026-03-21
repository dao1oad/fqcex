#!/usr/bin/env sh
set -eu

usage() {
  echo "usage: deploy/scripts/rollback.sh <previous-image-tag> [env-file]" >&2
  exit 1
}

if [ "$#" -lt 1 ]; then
  usage
fi

PREVIOUS_TAG="$1"
SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
PROJECT_ROOT=$(CDPATH= cd -- "$SCRIPT_DIR/../.." && pwd)
ENV_FILE="${2:-$PROJECT_ROOT/deploy/.env}"
COMPOSE_FILE="$PROJECT_ROOT/deploy/docker-compose.yml"
TMP_ENV=$(mktemp "${TMPDIR:-/tmp}/perp-platform-rollback.XXXXXX")

cleanup() {
  rm -f "$TMP_ENV"
}

trap cleanup EXIT INT TERM

if [ ! -f "$ENV_FILE" ]; then
  echo "missing env file: $ENV_FILE" >&2
  exit 1
fi

if ! command -v docker >/dev/null 2>&1; then
  echo "docker is required but was not found in PATH" >&2
  exit 1
fi

if docker compose version >/dev/null 2>&1; then
  DOCKER_COMPOSE_BIN="docker compose"
elif command -v docker-compose >/dev/null 2>&1 && docker-compose version >/dev/null 2>&1; then
  DOCKER_COMPOSE_BIN="docker-compose"
else
  echo "docker compose or docker-compose is required but is not available" >&2
  exit 1
fi

IMAGE_REPO=$(awk -F= '/^PERP_PLATFORM_IMAGE_REPO=/{print $2}' "$ENV_FILE")
if [ -z "$IMAGE_REPO" ]; then
  IMAGE_REPO="perp-platform"
fi

TARGET_IMAGE="${IMAGE_REPO}:${PREVIOUS_TAG}"

if ! docker image inspect "$TARGET_IMAGE" >/dev/null 2>&1; then
  echo "target image is not available locally: $TARGET_IMAGE" >&2
  exit 1
fi

awk -v previous_tag="$PREVIOUS_TAG" '
BEGIN { replaced = 0 }
$0 ~ /^PERP_PLATFORM_IMAGE_TAG=/ {
  print "PERP_PLATFORM_IMAGE_TAG=" previous_tag
  replaced = 1
  next
}
{ print }
END {
  if (replaced == 0) {
    print "PERP_PLATFORM_IMAGE_TAG=" previous_tag
  }
}
' "$ENV_FILE" > "$TMP_ENV"

echo "rolling back to ${TARGET_IMAGE}"
LIVE_CANARY_ENV_FILE="$TMP_ENV" sh -c "$DOCKER_COMPOSE_BIN --env-file \"$TMP_ENV\" -f \"$COMPOSE_FILE\" up -d --no-build --force-recreate control-plane operator-ui"

CONTROL_PLANE_PORT=$(awk -F= '/^CONTROL_PLANE_PORT=/{print $2}' "$TMP_ENV")
if [ -z "$CONTROL_PLANE_PORT" ]; then
  CONTROL_PLANE_PORT=8080
fi

OPERATOR_UI_PORT=$(awk -F= '/^OPERATOR_UI_PORT=/{print $2}' "$TMP_ENV")
if [ -z "$OPERATOR_UI_PORT" ]; then
  OPERATOR_UI_PORT=4173
fi

python3 -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:${CONTROL_PLANE_PORT}/control-plane/v1/health'); urllib.request.urlopen('http://127.0.0.1:${OPERATOR_UI_PORT}/'); print('rollback stack healthy')"
