# Codex Cloud Dry Run Runbook

## 目标

用一次可审计的 GitHub -> Codex cloud dry run，验证本仓库已经可以把后续 child issue 从本地执行切换到云端执行，同时不突破 `#91`、`#92`、`#93` 已冻结的 setup、安全和 orchestrator 边界。

## 先决条件

- 仓库已配置 Codex cloud environment
- `scripts/codex_cloud_setup.sh` 可用于 Linux/Bash setup
- cloud environment / secrets / network 约束已按 `docs/runbooks/codex-cloud-security.md` 配置
- orchestrator 已支持 portable dispatch pack 和 `accept --dispatch-path`
- 当前任务属于文档、测试、静态校验或 bounded code-change 范围

## 触发入口

在 GitHub PR 上触发 Codex：

- `@codex review`：请求 Codex review 当前 PR
- 非 `review` 的 `@codex ...` comment：启动一个 Codex cloud task

推荐 dry run comment：

```text
@codex summarize the cloud handoff in this PR and confirm whether later child issues can be executed in Codex cloud using the documented workflow. Do not make code changes.
```

## 操作步骤

1. 从对应 `type/task` issue 创建分支
2. 推送分支并打开 PR
3. 在 PR comment 中留下 bounded `@codex ...` 请求
4. 等待 Codex 回复或 review
5. 记录 PR URL、Trigger Comment URL、Codex Response URL 和 outcome
6. 如 dry run 成功，把 evidence 写回 PR 和仓库文档
7. 如 dry run 失败，按失败处置回退到本地执行或人工排障

## 失败处置

以下情况都视为 dry run 失败：

- `@codex` comment 没有触发任何响应
- Codex 明确提示仓库未接入或 environment 不可用
- Codex 请求真实交易凭证或越过 cloud security boundary
- Codex task 无法在 PR 上产出可审计结果

失败时执行：

1. 不把后续 issue 直接切到云端
2. 保留 PR、comment 和日志链接
3. 优先检查 Codex cloud / GitHub integration 设置
4. 必要时回退到本地执行，直到 dry run 打通

## Dry Run Record

- Date: `2026-03-19`
- PR URL: `pending`
- Trigger Comment URL: `pending`
- Codex Response URL: `pending`
- Outcome: `pending`

## 相关文档

- [Codex Cloud Setup](codex-cloud-setup.md)
- [Codex Cloud Security](codex-cloud-security.md)
- [Issue Orchestrator Runbook](issue-orchestrator.md)
