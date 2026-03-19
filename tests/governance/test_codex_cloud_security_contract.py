from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]


def read_text(path: str) -> str:
    return (REPO_ROOT / path).read_text(encoding="utf-8")


def test_security_documents_codex_cloud_secret_boundaries() -> None:
    content = read_text("SECURITY.md")

    assert "Codex cloud" in content
    assert "environment variables" in content
    assert "setup script" in content
    assert "agent phase" in content
    assert "BYBIT_API_KEY" in content
    assert "真实交易凭证" in content


def test_codex_cloud_architecture_freezes_two_phase_runtime_and_network_defaults() -> None:
    content = read_text("docs/architecture/CODEX_CLOUD_BOUNDARIES.md")

    assert "two-phase runtime" in content
    assert "setup script" in content
    assert "agent phase" in content
    assert "默认关闭网络访问" in content
    assert "`GET`" in content
    assert "`HEAD`" in content
    assert "`OPTIONS`" in content


def test_codex_cloud_runbook_documents_allowed_environment_values_and_allowlist() -> None:
    content = read_text("docs/runbooks/codex-cloud-security.md")

    assert "PERP_PLATFORM_ENVIRONMENT=test" in content
    assert "PYTHONUNBUFFERED=1" in content
    assert "PIP_DISABLE_PIP_VERSION_CHECK=1" in content
    assert "developers.openai.com" in content
    assert "platform.openai.com" in content
    assert "github.com" in content
    assert "api.github.com" in content
    assert "None" in content
    assert "不接入真实交易凭证" in content


def test_readme_links_codex_cloud_security_documents() -> None:
    content = read_text("README.md")

    assert "docs/runbooks/codex-cloud-security.md" in content
    assert "docs/architecture/CODEX_CLOUD_BOUNDARIES.md" in content
    assert "真实交易凭证" in content
