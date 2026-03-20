# Issue 59 WebSocket Disconnect Injector Design

## Goal

为 Phase 3 故障注入工具增加最小的 WebSocket 断连注入器，产出一个可审计、可复用的断连注入计划文件或标准输出结果。

## Recommendation

本任务采用“**生成注入计划**”而不是“直接强杀连接”的做法：

- 脚本负责验证输入、标准化断连注入参数、输出 JSON 注入计划
- 计划可打印到 stdout，也可写入指定文件
- 真正的执行可由后续操作员步骤或外部 harness 消费

这样可以避免把临时的本机网络破坏逻辑直接塞进仓库，同时满足当前 issue 的最小交付边界。

## Scope

新增 `scripts/inject_ws_disconnect.py`，支持：

- `--venue`
- `--stream` (`public` / `private` / `all`)
- `--duration-seconds`
- `--instrument-id`（可选）
- `--reason`（可选）
- `--output`（可选，写文件）

输出 JSON 字段：

- `injector`
- `venue`
- `stream`
- `duration_seconds`
- `instrument_id`
- `reason`
- `action`

其中 `action` 固定为 `disconnect_websocket`。

## Testing

新增 `tests/ops/test_ws_disconnect_injector.py`，覆盖：

1. 默认输出到 stdout
2. 参数被标准化到 JSON
3. 非法 duration 被拒绝

## Non-goals

- 不直接操作 Docker、iptables、进程句柄或真实 socket
- 不提前实现私有流静默与对账差异注入
- 不在本任务中修改 runbook
