# ACTIVE_WORK

## 当前分支定位

- `main`
  - 当前主分支，已合并治理基础和项目记忆系统。
  - 目前仍未包含 `perp-platform` 应用骨架和完整交付基座。
- `codex/ci-cd-bootstrap`
  - 基于旧基线携带 2 个未合并提交，内容方向对应 `#79-#83`。
  - 当前状态：只能作为参考分支，不能直接视为可合并结果。
- `codex/perp-platform-bootstrap`
  - worktree 仍在，但分支相对 `main` 已无独有提交。
  - 当前状态：属于陈旧工作区，不再代表当前应用骨架进度。

## 活跃工作结论

- 项目当前的治理和上下文恢复入口已经进入 `main`。
- 代码主线仍分散在多个未合并 feature branches。
- 交付链路现已通过 `#79-#83` 进入正式 backlog。
- 应用骨架应直接按 `#10` 及其 child issues 推进，而不是依赖陈旧 worktree。

## 当前风险

- 多个未合并工作并行存在，必须依靠 worktree、branch 和文档记忆系统区分状态。
- 不要把 feature branch 的内容写成 `main` 已经拥有的能力。
- 如果分支状态变化，先运行快照脚本，再更新这里和其他手工记忆入口。

## 下一步建议

- 再执行 `#25-#27`，建立 `perp-platform` 最小应用骨架。
- 然后执行 `#81-#83`，把 CI、部署脚本和 smoke / rollback 基座落回主线。
- 接着按 `#28-#38` 完成 Phase 1 核心闭环。
- 每次合并或删除分支后，重新运行 `py scripts/update_project_memory.py`。
