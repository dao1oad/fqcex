# Issue Orchestrator Runbook

## 目标

该 runbook 约束主 agent 如何按正确顺序推进 child issue，并在不破坏治理规则的前提下使用必要并发。

## 基本规则

- 只允许从 `type/task` issue 直接进入实现
- issue 顺序以 `ISSUE_HIERARCHY.md` 为准
- 一个 issue 在任一时刻只能有一个 `single writer`
- sidecar 只允许做只读探索、验证和预审
- merge、close 和最终 acceptance 只能由主 agent 执行

## 模型要求

- 主 agent 必须使用 `gpt-5.4`
- subagent 必须使用 `gpt-5.4`
- reasoning effort 固定为 `xhigh`

## 一次性确认

- 用户只和主 agent 确认方案
- 主 agent 把确认写入 `approval bundle`
- subagent 收到已批准的推荐方案后直接执行，不再重复向用户确认普通实现分歧
- 只有命中治理、架构、范围或冻结边界冲突时，subagent 才回主 agent 请求新决策

## 第二阶段入口

主 agent 当前推荐启动顺序：

1. `approval create`
2. `gh sync`
3. `start`

其中：

- `gh sync` 负责把 GitHub issue 元数据规范化到本地 `.codex/orchestrator/issues.json`
- `start` 负责串联同步、选下一个 ready issue、claim，并输出完整 dispatch pack
- 对开放的 `type/task` hierarchy drift 必须 `fail closed`

`start` 当前不会自动派发 subagent，也不会自动 merge 或 close issue；这些动作仍由主 agent 会话显式执行。

## Cloud Mode

本地模式仍可继续使用 `.codex/orchestrator/state.json` 记录 runtime state。

当主 agent 需要把任务切到 GitHub / cloud task 执行时，推荐使用 portable dispatch pack，而不是依赖当前本机会话的 state 文件。

推荐命令顺序：

1. `approval create`
2. `gh sync`
3. `start --skip-state-save --dispatch-path <dispatch.json>`
4. cloud task 根据 dispatch pack 执行
5. `accept --dispatch-path <dispatch.json>`

portable dispatch pack 当前至少包含：

- `execution_context`
- `constraints`
- `claim_record`
- `acceptance_payload`
- `subagent_prompt`

这样 cloud task 只要带回：

- 当前 `head_sha`
- changed files
- review evidence

主 agent 就可以在不读取本地旧 `state.json` 的情况下完成 acceptance。

## 必要并发

- issue 级别严格串行
- issue 内允许一个 writer 和最多两个只读 sidecar
- `CONTEXT_GATHERING`、`VERIFYING`、`NEXT_ISSUE_PREFETCH` 可以启用必要并发
- `IMPLEMENTING` 阶段禁止第二个 writer

## 状态与阻塞

- runtime state 记录当前 active issue、branch、worktree、agent id、SHA 和 blocker
- 如果需要新 sibling issue、需要更新 ADR/runbook/Phase 边界、或连续失败不收敛，主 agent 必须标记 `BLOCKED`
- `BLOCKED` 后停止自动推进后续 issue

## Acceptance

主 agent 在合并前至少检查：

- issue 范围未越界
- 当前 `head SHA` 与验证结果一致
- changed files 落在允许边界内
- review evidence 已存在
- 需要的治理文档已更新

## Dispatch Pack

`prepare` 和 `start` 当前都会输出：

- `execution_context`
- `constraints`
- `subagent_prompt`

该输出用于直接驱动 `gpt-5.4` / `xhigh` subagent，但主 agent 仍保留最终 acceptance 和 merge 决策权。
