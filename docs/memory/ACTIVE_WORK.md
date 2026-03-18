# ACTIVE_WORK

## 当前分支定位

- `main`
  - 当前主分支，仅保留治理和文档基础。
  - 不是最新功能主线。
- `codex/ci-cd-bootstrap`
  - 已完成 CI/CD、Playwright smoke、Docker Compose 自动部署骨架。
  - 当前状态：未合并到 `main`。
- `codex/project-memory-system`
  - 当前工作分支。
  - 负责建立项目记忆系统文档。
  - 当前状态：进行中。
- `codex/perp-platform-bootstrap`
  - 已建立最小 Python 应用骨架与测试基础。
  - 当前状态：未合并到 `main`。

## 活跃工作结论

- 项目当前的代码主线不在 `main`，而在多个未合并 feature branches。
- `codex/ci-cd-bootstrap` 负责交付链路。
- `codex/perp-platform-bootstrap` 负责应用骨架。
- `codex/project-memory-system` 负责让后续新会话快速恢复上下文。

## 当前风险

- 多个未合并工作并行存在，必须依靠 worktree、branch 和文档记忆系统区分状态。
- 不要把 feature branch 的内容写成 `main` 已经拥有的能力。
- 后续如果分支状态变化，先更新这里，再更新其他记忆入口。

## 下一步建议

- 优先补齐自动项目快照脚本。
- 之后把 `SESSION_HANDOFF` 固化成新会话入口。
- 再把记忆系统接入仓库根入口文档。
