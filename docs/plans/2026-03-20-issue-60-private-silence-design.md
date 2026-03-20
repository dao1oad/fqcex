# Issue 60 Private Silence Injector Design

## Goal

增加一个私有流静默注入器脚本，生成可审计的注入计划，用于模拟用户流在指定持续时间内不再产生事件。

## Recommendation

继续沿用 `#59` 的“输出注入计划，不直接改写运行进程”模式：

- 输入 venue、duration、scope、reason
- 输出 JSON 注入计划到 stdout 或文件
- 保持脚本本身无副作用，方便 runbook 引用和人工执行

## Scope

新增 `scripts/inject_private_silence.py`：

- `--venue`
- `--duration-seconds`
- `--scope`（默认 `account`）
- `--reason`
- `--output`

输出字段：

- `injector`
- `venue`
- `scope`
- `duration_seconds`
- `reason`
- `action`

其中 `action` 固定为 `silence_private_stream`。

## Testing

新增 `tests/ops/test_private_silence_injector.py`，覆盖：

1. stdout 输出的 JSON 结构
2. 非法 duration 拒绝
