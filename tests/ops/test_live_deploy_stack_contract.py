from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
COMPOSE_PATH = REPO_ROOT / "deploy" / "docker-compose.yml"
DEPLOY_SCRIPT_PATH = REPO_ROOT / "deploy" / "scripts" / "deploy.sh"
BOOTSTRAP_SCRIPT_PATH = REPO_ROOT / "deploy" / "scripts" / "bootstrap-server.sh"
ROLLBACK_SCRIPT_PATH = REPO_ROOT / "deploy" / "scripts" / "rollback.sh"
PYTHON_DOCKERFILE_PATH = REPO_ROOT / "deploy" / "Dockerfile"
UI_DOCKERFILE_PATH = REPO_ROOT / "deploy" / "operator-ui.Dockerfile"
ACCEPTANCE_RUNBOOK_PATH = REPO_ROOT / "docs" / "runbooks" / "live-canary-acceptance.md"


def test_compose_declares_control_plane_and_operator_ui_services() -> None:
    content = COMPOSE_PATH.read_text(encoding="utf-8")

    assert "control-plane:" in content
    assert "operator-ui:" in content
    assert '${LIVE_CANARY_ENV_FILE:-.env}' in content
    assert '${CONTROL_PLANE_BIND_ADDRESS:-127.0.0.1}:${CONTROL_PLANE_PORT:-8080}:8080' in content
    assert '${OPERATOR_UI_BIND_ADDRESS:-127.0.0.1}:${OPERATOR_UI_PORT:-4173}:80' in content
    assert "restart: unless-stopped" in content


def test_control_plane_service_uses_control_plane_module_entrypoint() -> None:
    content = COMPOSE_PATH.read_text(encoding="utf-8")

    assert 'command: ["python", "-m", "perp_platform.control_plane"' in content


def test_operator_ui_has_dedicated_deploy_dockerfile() -> None:
    assert UI_DOCKERFILE_PATH.exists()


def test_deploy_script_uses_compose_up_for_long_running_services() -> None:
    content = DEPLOY_SCRIPT_PATH.read_text(encoding="utf-8")

    assert "docker compose" in content
    assert "up -d" in content
    assert 'ENV_FILE="${1:-$PROJECT_ROOT/deploy/.env}"' in content
    assert "rm -sf control-plane operator-ui" in content


def test_bootstrap_script_accepts_explicit_env_path() -> None:
    content = BOOTSTRAP_SCRIPT_PATH.read_text(encoding="utf-8")

    assert 'ENV_FILE="${1:-$PROJECT_ROOT/deploy/.env}"' in content


def test_rollback_script_restarts_long_running_services() -> None:
    content = ROLLBACK_SCRIPT_PATH.read_text(encoding="utf-8")

    assert "docker compose" in content
    assert "up -d" in content
    assert '${IMAGE_REPO}-ui:${PREVIOUS_TAG}' in content
    assert "UI target image is not available locally" in content
    assert "rm -sf control-plane operator-ui" in content


def test_python_dockerfile_keeps_python_runtime_install_path() -> None:
    content = PYTHON_DOCKERFILE_PATH.read_text(encoding="utf-8")

    assert "python -m pip install" in content
    assert 'CMD ["python"' in content


def test_acceptance_runbook_exists() -> None:
    assert ACCEPTANCE_RUNBOOK_PATH.exists()


def test_acceptance_runbook_matches_hardened_runtime_contract() -> None:
    content = ACCEPTANCE_RUNBOOK_PATH.read_text(encoding="utf-8")

    assert "docker compose` 或 `docker-compose" in content
    assert "CONTROL_PLANE_PORT" in content
    assert "OPERATOR_UI_PORT" in content
    assert "python3" in content
