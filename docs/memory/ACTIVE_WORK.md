# ACTIVE_WORK

## 当前分支定位

- `main`
  - 当前主分支，已合并治理基础和项目记忆系统。
  - 目前仍未包含 CI/CD 骨架和应用骨架。
- `codex/ci-cd-bootstrap`
  - 已完成 CI/CD、Playwright smoke、Docker Compose 自动部署骨架。
  - 当前状态：未合并到 `main`。
- `codex/perp-platform-bootstrap`
  - 已建立最小 Python 应用骨架与测试基础。
  - 当前状态：未合并到 `main`。

## 活跃工作结论

- 项目当前的治理和上下文恢复入口已经进入 `main`。
- 代码主线仍分散在多个未合并 feature branches。
- `codex/ci-cd-bootstrap` 负责交付链路。
- `codex/perp-platform-bootstrap` 负责应用骨架。

## 当前风险

- 多个未合并工作并行存在，必须依靠 worktree、branch 和文档记忆系统区分状态。
- 不要把 feature branch 的内容写成 `main` 已经拥有的能力。
- 如果分支状态变化，先运行快照脚本，再更新这里和其他手工记忆入口。

## 下一步建议

- 优先评估并合并 `codex/ci-cd-bootstrap`。
- 然后推进 `codex/perp-platform-bootstrap`，让 Phase 1 有最小可运行骨架。
- 每次合并或删除分支后，重新运行 `py scripts/update_project_memory.py`。
