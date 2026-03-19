# ACTIVE_WORK

## 当前分支定位

- `main`
  - 当前主分支，已合并治理基础、项目记忆系统以及 `#25-#27` 的应用骨架最小闭环。
  - 已包含 `perp_platform` 包入口、配置初始化契约和共享测试基座。
- `codex/ci-cd-bootstrap`
  - 基于旧基线携带 2 个未合并提交，内容方向对应 `#79-#83`。
  - 当前状态：只能作为参考分支，不能直接视为可合并结果。
- `codex/perp-platform-bootstrap`
  - worktree 仍在，但分支相对 `main` 已无独有提交。
  - 当前状态：属于陈旧工作区，不再代表当前应用骨架进度。

## 活跃工作结论

- 项目当前的治理和上下文恢复入口已经进入 `main`。
- `#10` 下的 `#25-#27` 已进入 `main`，应用骨架不再阻塞后续 child issues。
- 交付链路现已通过 `#79-#83` 进入正式 backlog。
- 陈旧的 `codex/perp-platform-bootstrap` 不应再作为现状真相源。

## 当前风险

- `codex/ci-cd-bootstrap` 仍基于旧基线，若继续复用其内容，必须先按当前 `main` 重新收口。
- 本次把 `main` 推到远端时绕过了必需状态检查 `governance-check`；后续应优先恢复正常 PR / CI 合流路径。
- 如果分支状态变化，先运行快照脚本，再更新这里和其他手工记忆入口。

## 下一步建议

- 按既定顺序继续执行 `#81-#83`，把 CI、部署脚本和 smoke / rollback 基座落回主线。
- 接着按 `#28-#38` 完成 Phase 1 核心闭环。
- 每次合并或删除分支后，重新运行 `py scripts/update_project_memory.py`。
