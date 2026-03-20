# Issue 62 Injector Runbooks Design

## Goal

把 `#59`、`#60`、`#61` 的故障注入脚本接入运行手册，明确操作员如何生成注入计划、记录 incident 和恢复后的处置动作。

## Recommendation

本任务只修改 runbook，不新增脚本能力：

- `incident-template.md` 增加 fault injection 记录字段
- `public-stream-recovery.md` 引用 WebSocket 断连注入器
- `private-stream-recovery.md` 引用私有流静默与对账差异注入器

## Scope

文档应覆盖：

- 运行脚本的命令示例
- 产出 JSON 注入计划的保存位置
- 执行后需要在 incident 中记录的字段
- 何时停止演练并升级 `REDUCE_ONLY` / `BLOCKED`
