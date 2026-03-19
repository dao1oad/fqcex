from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]


def read_text(path: str) -> str:
    return (REPO_ROOT / path).read_text(encoding="utf-8")


def test_codex_cloud_setup_script_exists_and_installs_package() -> None:
    script_path = REPO_ROOT / "scripts" / "codex_cloud_setup.sh"

    assert script_path.exists()
    content = script_path.read_text(encoding="utf-8")
    assert "#!/usr/bin/env bash" in content
    assert "python -m pip install --upgrade pip" in content
    assert "python -m pip install -e ." in content


def test_readme_documents_linux_bash_setup_and_verification() -> None:
    content = read_text("README.md")

    assert "Codex cloud" in content or "Linux/Bash" in content
    assert "python -m pip install -e ." in content
    assert "python -m pytest tests -q" in content


def test_agents_memory_entry_uses_python_and_marks_powershell_optional() -> None:
    content = read_text("AGENTS.md")

    assert "python scripts/update_project_memory.py" in content
    assert "Windows-only" in content
    assert "scripts/project_context.ps1" in content


def test_codex_cloud_runbook_documents_setup_and_verification() -> None:
    content = read_text("docs/runbooks/codex-cloud-setup.md")

    assert "scripts/codex_cloud_setup.sh" in content
    assert "python -m pytest tests -q" in content
