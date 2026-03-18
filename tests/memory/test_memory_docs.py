from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]


def test_memory_docs_exist() -> None:
    assert (REPO_ROOT / "docs" / "memory" / "PROJECT_STATE.md").is_file()
    assert (REPO_ROOT / "docs" / "memory" / "ACTIVE_WORK.md").is_file()
    assert (REPO_ROOT / "docs" / "memory" / "SESSION_HANDOFF.md").is_file()
    assert (REPO_ROOT / "docs" / "memory" / "generated" / ".gitkeep").is_file()
