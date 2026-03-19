from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]


def read_text(path: str) -> str:
    return (REPO_ROOT / path).read_text(encoding="utf-8")


def test_smoke_and_rollback_files_exist() -> None:
    expected_files = [
        ".github/workflows/cd.yml",
        "package.json",
        "package-lock.json",
        "playwright.config.ts",
        "tests/e2e/fixtures/index.html",
        "tests/e2e/smoke.spec.ts",
        "deploy/scripts/rollback.sh",
        "docs/runbooks/rollback.md",
    ]

    for path in expected_files:
        assert (REPO_ROOT / path).exists(), path


def test_cd_workflow_is_manual_and_runs_smoke_steps() -> None:
    content = read_text(".github/workflows/cd.yml")

    assert "workflow_dispatch:" in content
    assert "bash deploy/scripts/deploy.sh" in content
    assert "npm ci" in content
    assert "npx playwright test" in content


def test_package_and_playwright_config_define_smoke_baseline() -> None:
    package_json = read_text("package.json")
    playwright_config = read_text("playwright.config.ts")

    assert '"smoke:e2e"' in package_json
    assert "@playwright/test" in package_json
    assert 'testDir: "./tests/e2e"' in playwright_config


def test_rollback_script_requires_explicit_tag_and_no_build() -> None:
    content = read_text("deploy/scripts/rollback.sh")

    assert "usage: deploy/scripts/rollback.sh <previous-image-tag> [env-file]" in content
    assert "PERP_PLATFORM_IMAGE_TAG" in content
    assert "--no-build" in content


def test_rollback_runbook_documents_explicit_tag_and_failure_path() -> None:
    content = read_text("docs/runbooks/rollback.md")

    assert "# 回滚 Runbook" in content
    assert "previous image tag" in content
    assert "deploy/scripts/rollback.sh" in content
    assert "失败" in content


def test_gitignore_covers_node_and_playwright_artifacts() -> None:
    content = read_text(".gitignore")

    assert "node_modules/" in content
    assert "playwright-report/" in content
    assert "test-results/" in content
