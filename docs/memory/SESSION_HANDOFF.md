# SESSION_HANDOFF

## 新会话先看什么

1. `docs/memory/PROJECT_STATE.md`
2. `docs/memory/ACTIVE_WORK.md`
3. `docs/memory/generated/project_snapshot.md`
4. `docs/roadmap/ISSUE_HIERARCHY.md`
5. `docs/roadmap/ROADMAP.md`
6. `docs/architecture/ARCHITECTURE.md`
7. `docs/plans/dry-run-closeout.md`

## 新会话先跑什么

```powershell
git status --short --branch
git fetch origin
git merge --ff-only origin/main
git worktree list
git log --oneline -10 origin/main
py scripts/update_project_memory.py
```

## 当前建议切入点

- 不要再从 Phase 1-3 的旧 worktree 恢复开发。
- 直接以当前 `main` 为基线，按 Phase 4 顺序从 `#67` 开始。
- 如果会话目标涉及 issue / PR / 分支 / worktree 状态，先运行 `py scripts/update_project_memory.py`。

## 注意事项

- `docs/plans/dry-run-evidence.md` 和 `docs/plans/dry-run-closeout.md` 已经是 Phase 3 的正式结论入口。
- Phase 3 的结论只代表 `repository-scoped` 干跑，不要在后续文档里误写成真实交易所 live/testnet 已验证。
- `.codex/` 是本地运行态目录；需要主线真相时，以 GitHub issue / PR、`origin/main` 和仓库文档为准。
