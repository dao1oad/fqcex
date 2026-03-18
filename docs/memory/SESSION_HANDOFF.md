# SESSION_HANDOFF

## 新会话先看什么

1. `docs/memory/PROJECT_STATE.md`
2. `docs/memory/ACTIVE_WORK.md`
3. `README.md`
4. `docs/roadmap/ROADMAP.md`
5. `docs/architecture/ARCHITECTURE.md`
6. `docs/plans/2026-03-18-project-memory-system-design.md`

## 新会话先跑什么

```powershell
git status --short --branch
git branch --all
git worktree list
git log --oneline -10
```

如果已经有快照脚本，再补跑：

```powershell
python scripts/update_project_memory.py
```

## 当前建议切入点

- 如果要继续完善治理和上下文恢复，先补自动快照脚本，再补仓库根入口说明。
- 如果要继续开发交付能力，优先看 `codex/ci-cd-bootstrap` 分支。
- 如果要继续开发应用骨架，优先看 `codex/perp-platform-bootstrap` 分支。

## 注意事项

- 任何会改变 Phase 1 边界、主架构、运行安全规则的改动，都先更新记忆文件和治理文档。
- 任何 feature branch 的成果都不要直接当成 `main` 的已完成状态。
