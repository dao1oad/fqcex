# Issue 61 Reconcile Diff Injector Design

## Goal

增加一个对账差异注入器脚本，输出标准化的 reconcile diff 注入计划，用于模拟订单、仓位或余额差异。

## Recommendation

本任务仍然只生成注入计划，不直接改写数据库或 Supervisor 状态：

- 输入 venue、resource、diff kind、instrument
- 输出 JSON 注入计划
- 为后续 runbook 和干跑证据提供统一结构

## Scope

新增 `scripts/inject_reconcile_diff.py`：

- `--venue`
- `--resource` (`order` / `position` / `balance`)
- `--diff-kind` (`missing` / `extra` / `mismatch`)
- `--instrument-id`（可选）
- `--reason`
- `--output`

输出字段：

- `injector`
- `venue`
- `resource`
- `diff_kind`
- `instrument_id`
- `reason`
- `action`

其中 `action` 固定为 `inject_reconcile_diff`。

## Testing

新增 `tests/ops/test_reconcile_diff_injector.py`，覆盖：

1. stdout 输出 JSON
2. `balance` 场景可不带 instrument
3. 非法 diff kind 拒绝
