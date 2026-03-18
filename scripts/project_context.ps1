$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot

# Recommended commands for new sessions:
# git status --short --branch
# git worktree list
# py scripts/update_project_memory.py

Write-Host "Repository Root: $repoRoot"
Write-Host ""
Write-Host "Memory Entry Points:"
Write-Host "- docs/memory/PROJECT_STATE.md"
Write-Host "- docs/memory/ACTIVE_WORK.md"
Write-Host "- docs/memory/SESSION_HANDOFF.md"
Write-Host "- docs/memory/generated/project_snapshot.md"
Write-Host ""
Write-Host "Current Branch:"
git -C $repoRoot status --short --branch
Write-Host ""
Write-Host "Worktrees:"
git -C $repoRoot worktree list
Write-Host ""
Write-Host "Recent Commits:"
git -C $repoRoot log --oneline -10
