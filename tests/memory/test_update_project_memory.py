import importlib.util
from pathlib import Path
from subprocess import CompletedProcess
from subprocess import run


REPO_ROOT = Path(__file__).resolve().parents[2]
SNAPSHOT_PATH = REPO_ROOT / "docs" / "memory" / "generated" / "project_snapshot.md"
SCRIPT_PATH = REPO_ROOT / "scripts" / "update_project_memory.py"


def load_module():
    spec = importlib.util.spec_from_file_location("update_project_memory", SCRIPT_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_update_project_memory_generates_snapshot() -> None:
    if SNAPSHOT_PATH.exists():
        SNAPSHOT_PATH.unlink()

    result = run(
        ["py", str(SCRIPT_PATH)],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert SNAPSHOT_PATH.is_file()

    content = SNAPSHOT_PATH.read_text(encoding="utf-8")

    assert "Current Branch" in content
    assert "Worktrees" in content
    assert "Recent Commits" in content
    assert "Repository Docs" in content


def test_update_project_memory_handles_missing_github_metadata(monkeypatch) -> None:
    module = load_module()

    def fake_run_command(repo_root: Path, *args: str) -> CompletedProcess[str]:
        if args[:2] == ("gh", "issue") or args[:2] == ("gh", "pr"):
            return CompletedProcess(args=args, returncode=1, stdout="", stderr="gh unavailable")
        return CompletedProcess(args=args, returncode=0, stdout="ok", stderr="")

    monkeypatch.setattr(module, "run_command", fake_run_command)

    content = module.build_snapshot(REPO_ROOT)

    assert "GitHub metadata unavailable" in content


def test_update_project_memory_handles_missing_gh_binary(monkeypatch) -> None:
    module = load_module()

    def fake_run_command(repo_root: Path, *args: str) -> CompletedProcess[str]:
        if args[:2] == ("gh", "issue") or args[:2] == ("gh", "pr"):
            raise FileNotFoundError("gh not installed")
        return CompletedProcess(args=args, returncode=0, stdout="ok", stderr="")

    monkeypatch.setattr(module, "run_command", fake_run_command)

    content = module.build_snapshot(REPO_ROOT)

    assert "GitHub metadata unavailable" in content


def test_update_project_memory_prefers_github_api_for_remote_branches(monkeypatch) -> None:
    module = load_module()

    def fake_run_command(repo_root: Path, *args: str) -> CompletedProcess[str]:
        if args[:4] == ("gh", "repo", "view", "--json"):
            return CompletedProcess(args=args, returncode=0, stdout="dao1oad/fqcex", stderr="")
        if args[:3] == ("gh", "api", "repos/dao1oad/fqcex/branches"):
            return CompletedProcess(
                args=args,
                returncode=0,
                stdout="main\ncodex/ci-cd-bootstrap",
                stderr="",
            )
        if args[:3] == ("git", "branch", "--remotes"):
            return CompletedProcess(
                args=args,
                returncode=0,
                stdout="origin/main\norigin/stale-branch",
                stderr="",
            )
        return CompletedProcess(args=args, returncode=0, stdout="ok", stderr="")

    monkeypatch.setattr(module, "safe_run_command", fake_run_command)

    content = module.build_snapshot(REPO_ROOT)

    assert "main\ncodex/ci-cd-bootstrap" in content
    assert "origin/stale-branch" not in content


def test_update_project_memory_includes_current_repository_context() -> None:
    result = run(
        ["py", str(SCRIPT_PATH)],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr

    content = SNAPSHOT_PATH.read_text(encoding="utf-8")

    assert "## main...origin/main" in content
    assert "codex/ci-cd-bootstrap" in content
    assert "Local Branches" in content
    assert "Remote Branches" in content
    assert "docs/memory/PROJECT_STATE.md" in content


def test_update_project_memory_excludes_generated_snapshot_from_status(monkeypatch) -> None:
    module = load_module()
    calls: list[tuple[str, ...]] = []

    def fake_run_command(repo_root: Path, *args: str) -> CompletedProcess[str]:
        calls.append(args)
        return CompletedProcess(args=args, returncode=0, stdout="ok", stderr="")

    monkeypatch.setattr(module, "safe_run_command", fake_run_command)

    module.build_snapshot(REPO_ROOT)

    assert any(
        args[:3] == ("git", "status", "--short")
        and ":(exclude)docs/memory/generated/project_snapshot.md" in args
        for args in calls
    )
