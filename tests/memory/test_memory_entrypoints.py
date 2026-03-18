from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]


def test_readme_references_memory_system() -> None:
    content = (REPO_ROOT / "README.md").read_text(encoding="utf-8")

    assert "docs/memory/PROJECT_STATE.md" in content
    assert "scripts/project_context.ps1" in content


def test_agents_references_memory_bootstrap() -> None:
    content = (REPO_ROOT / "AGENTS.md").read_text(encoding="utf-8")

    assert "docs/memory/PROJECT_STATE.md" in content
    assert "scripts/update_project_memory.py" in content
