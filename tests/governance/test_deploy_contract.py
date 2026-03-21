from pathlib import Path
from subprocess import run


REPO_ROOT = Path(__file__).resolve().parents[2]


def read_text(path: str) -> str:
    return (REPO_ROOT / path).read_text(encoding="utf-8")


def read_git_mode(path: str) -> str:
    result = run(
        ["git", "ls-files", "--stage", path],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.split()[0]


def test_deploy_scaffold_files_exist() -> None:
    expected_files = [
        "deploy/.env.example",
        "deploy/Dockerfile",
        "deploy/docker-compose.yml",
        "deploy/scripts/bootstrap-server.sh",
        "deploy/scripts/deploy.sh",
        "docs/runbooks/deploy.md",
    ]

    for path in expected_files:
        assert (REPO_ROOT / path).exists(), path


def test_env_example_declares_minimal_deploy_contract() -> None:
    content = read_text("deploy/.env.example")

    assert "PERP_PLATFORM_APP_NAME=" in content
    assert "PERP_PLATFORM_ENVIRONMENT=" in content
    assert "PERP_PLATFORM_LOG_LEVEL=" in content
    assert "PERP_PLATFORM_IMAGE_REPO=" in content
    assert "PERP_PLATFORM_IMAGE_TAG=" in content


def test_dockerfile_builds_and_runs_control_plane() -> None:
    content = read_text("deploy/Dockerfile")

    assert "FROM python:3.12-slim" in content
    assert "apt-get install" in content
    assert "build-essential" in content
    assert "python -m pip install ." in content
    assert 'CMD ["python", "-m", "perp_platform.control_plane"' in content


def test_compose_defines_dual_service_live_stack() -> None:
    content = read_text("deploy/docker-compose.yml")

    assert "control-plane:" in content
    assert "operator-ui:" in content
    assert "env_file:" in content
    assert '${LIVE_CANARY_ENV_FILE:-.env}' in content
    assert 'image: "${PERP_PLATFORM_IMAGE_REPO}:${PERP_PLATFORM_IMAGE_TAG}"' in content


def test_bootstrap_and_deploy_scripts_define_expected_commands() -> None:
    bootstrap = read_text("deploy/scripts/bootstrap-server.sh")
    deploy = read_text("deploy/scripts/deploy.sh")

    assert "docker compose version" in bootstrap
    assert 'ENV_FILE="${1:-$PROJECT_ROOT/deploy/.env}"' in bootstrap
    assert "mkdir -p" in bootstrap
    assert "docker compose" in deploy
    assert "build" in deploy
    assert "up -d" in deploy
    assert 'ENV_FILE="${1:-$PROJECT_ROOT/deploy/.env}"' in deploy


def test_deploy_shell_scripts_are_tracked_as_executable() -> None:
    for path in [
        "deploy/scripts/bootstrap-server.sh",
        "deploy/scripts/deploy.sh",
        "deploy/scripts/preflight-live.sh",
        "deploy/scripts/rollback.sh",
    ]:
        assert read_git_mode(path) == "100755"


def test_deploy_runbook_documents_live_stack_steps_and_success_signal() -> None:
    content = read_text("docs/runbooks/deploy.md")

    assert "# 部署 Runbook" in content
    assert "前置条件" in content
    assert "deploy/scripts/bootstrap-server.sh" in content
    assert "deploy/scripts/deploy.sh" in content
    assert "Live Canary Preflight" in content
    assert "PERP_PLATFORM_IMAGE_TAG" in content
