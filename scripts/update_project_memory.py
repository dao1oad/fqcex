from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from subprocess import CompletedProcess, run


REPO_DOCS = [
    "README.md",
    "AGENTS.md",
    "docs/roadmap/ROADMAP.md",
    "docs/architecture/ARCHITECTURE.md",
    "docs/memory/PROJECT_STATE.md",
    "docs/memory/ACTIVE_WORK.md",
    "docs/memory/SESSION_HANDOFF.md",
]


def run_command(repo_root: Path, *args: str) -> CompletedProcess[str]:
    return run(
        list(args),
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )


def safe_run_command(repo_root: Path, *args: str) -> CompletedProcess[str]:
    try:
        return run_command(repo_root, *args)
    except FileNotFoundError as error:
        return CompletedProcess(args=args, returncode=127, stdout="", stderr=str(error))


def build_snapshot(repo_root: Path) -> str:
    current_branch = safe_run_command(
        repo_root,
        "git",
        "status",
        "--short",
        "--branch",
        "--",
        ".",
        ":(exclude)docs/memory/generated/project_snapshot.md",
    )
    local_branches = safe_run_command(repo_root, "git", "branch", "--format=%(refname:short)")
    remote_branches = safe_run_command(repo_root, "git", "branch", "--remotes", "--format=%(refname:short)")
    worktrees = safe_run_command(repo_root, "git", "worktree", "list")
    recent_commits = safe_run_command(repo_root, "git", "log", "--oneline", "-10")
    issues = safe_run_command(
        repo_root,
        "gh",
        "issue",
        "list",
        "--limit",
        "10",
    )
    pull_requests = safe_run_command(
        repo_root,
        "gh",
        "pr",
        "list",
        "--limit",
        "10",
    )

    lines = [
        "# Project Snapshot",
        "",
        f"Generated: {datetime.now(timezone.utc).isoformat()}",
        f"Repository Root: `{repo_root}`",
        "",
        "## Current Branch",
        "```text",
        current_branch.stdout.strip(),
        "```",
        "",
        "## Local Branches",
        "```text",
        local_branches.stdout.strip(),
        "```",
        "",
        "## Remote Branches",
        "```text",
        remote_branches.stdout.strip(),
        "```",
        "",
        "## Worktrees",
        "```text",
        worktrees.stdout.strip(),
        "```",
        "",
        "## Recent Commits",
        "```text",
        recent_commits.stdout.strip(),
        "```",
        "",
        "## Repository Docs",
    ]

    for relative_path in REPO_DOCS:
        status = "present" if (repo_root / relative_path).exists() else "missing"
        lines.append(f"- `{relative_path}`: {status}")

    lines.extend(["", "## GitHub Issues"])
    if issues.returncode == 0:
        lines.extend(["```text", issues.stdout.strip() or "(none)", "```"])
    else:
        lines.append("GitHub metadata unavailable: issues")

    lines.extend(["", "## GitHub Pull Requests"])
    if pull_requests.returncode == 0:
        lines.extend(["```text", pull_requests.stdout.strip() or "(none)", "```"])
    else:
        lines.append("GitHub metadata unavailable: pull requests")

    lines.append("")
    return "\n".join(lines)


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    snapshot_path = repo_root / "docs" / "memory" / "generated" / "project_snapshot.md"
    snapshot_path.parent.mkdir(parents=True, exist_ok=True)
    snapshot_path.write_text(build_snapshot(repo_root), encoding="utf-8")
    print(snapshot_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
