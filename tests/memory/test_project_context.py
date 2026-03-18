from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT_PATH = REPO_ROOT / "scripts" / "project_context.ps1"


def test_project_context_script_exists_with_memory_entrypoints() -> None:
    assert SCRIPT_PATH.is_file()

    content = SCRIPT_PATH.read_text(encoding="utf-8")

    assert "git status --short --branch" in content
    assert "git worktree list" in content
    assert "docs/memory/PROJECT_STATE.md" in content
