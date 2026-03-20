# Issue 58 Checker Signals Design

## Goal

把 `#57` 产出的 checker policy 结果映射成 `Supervisor` 可直接消费的中间信号，完成 checker tracking 的最小闭环，但不改写 `Supervisor` 现有状态机和 truth ownership。

## Context

- `#55` 已完成 checker bootstrap。
- `#56` 已完成顶档接入与归一化。
- `#57` 已完成 freshness / divergence policy。
- `Supervisor` 当前已有统一 `SupervisorState` 枚举和投影模型。

本任务只做 signal projection，不做：

- Supervisor 状态机改造
- checker 直接写入 Supervisor truth
- 新的恢复或风控规则

## Options

### Option A: 产出 supervisor-consumable signal，对应现有 `SupervisorState`

新增 `checker/signals.py`，输入 `CheckerPolicyResult`，输出：

- venue
- instrument_id
- suggested Supervisor state
- reason
- 原始策略诊断字段

优点：

- 最小闭环
- 直接复用现有 `SupervisorState`
- 不需要改 `supervisor/triggers.py`

缺点：

- 只是“可消费信号”，还不是正式写入状态机

### Option B: 直接修改 `SupervisorTriggerInputs`

把 checker stale/diverged 字段直接加入 Supervisor trigger 输入。

优点：

- 后续 wiring 更短

缺点：

- 超出当前 issue 边界
- 会把 checker 集成和 supervisor contract 改造混成一件事

### Option C: 只输出布尔值，不对接 `SupervisorState`

只产出 `healthy/stale/diverged` 布尔字段。

优点：

- 最简单

缺点：

- “Supervisor 可消费”语义太弱
- `#58` 完成后还需要额外翻译层

## Recommendation

选 **Option A**。

最小实现是把 checker policy 结果翻译成“对 Supervisor 有意义的状态建议”，但不宣称 checker 成为真相源。Supervisor 仍保留最终决策权。

## Mapping

默认映射：

- healthy -> `SupervisorState.LIVE`
- stale -> `SupervisorState.DEGRADED`
- diverged -> `SupervisorState.RESYNCING`

如果同时 `stale` 和 `diverged`：

- 取更严格的 `SupervisorState.RESYNCING`
- reason 使用 divergence 原因

推荐 reason 常量：

- `checker_healthy`
- `checker_stale`
- `checker_top_of_book_diverged`

## Design

新增 `CheckerSupervisorSignal`：

- `venue`
- `instrument_id`
- `suggested_state`
- `reason`
- `stale`
- `diverged`
- `age_seconds`
- `max_divergence_bps`

新增 `build_checker_supervisor_signal(policy_result)`：

- 输入 `CheckerPolicyResult`
- 输出 `CheckerSupervisorSignal`

这层只做纯映射，不引入外部依赖。

## Testing

新增 `tests/perp_platform/test_checker_signals.py`，覆盖：

1. healthy policy -> `LIVE`
2. stale only -> `DEGRADED`
3. diverged only -> `RESYNCING`
4. stale + diverged -> `RESYNCING`

## Docs

更新 `docs/architecture/ARCHITECTURE.md`：

- checker policy result 会先映射成 supervisor-consumable signal
- checker 只提供建议状态，不直接覆盖 Supervisor truth
