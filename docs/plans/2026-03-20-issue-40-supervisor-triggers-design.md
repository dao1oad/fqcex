# Issue 40 Supervisor Trigger Evaluation Design

## 背景

`#39` 已冻结 `SupervisorState` 和迁移契约，接下来需要把流信号和恢复故障信号映射成状态迁移结果。当前文档已给出最小规则：

- Public stream stale:
  - `DEGRADED` after 1.5s
  - `RESYNCING` after 3s
- Private stream stale:
  - `REDUCE_ONLY` after 10s
- Reconciliation failure:
  - `BLOCKED`
- Repeated recovery failure:
  - `BLOCKED`

`#40` 只负责求值逻辑，不负责 venue / instrument projection。

## 方案比较

### 方案 A：state-aware trigger evaluator，直接返回 `SupervisorTransition`

- 优点：直接消费 `#39` 的迁移契约
- 优点：可以避免“当前已在 `REDUCE_ONLY`，却因 public lag 被错误回退到 `RESYNCING`”这类非法结果
- 优点：后续 `#41` 只需要消费已求值的状态结果

### 方案 B：只返回目标状态，不知道当前状态

- 优点：实现更短
- 缺点：需要调用方自己处理非法迁移和严重程度优先级，职责会散到后续 issue

### 方案 C：现在就把 venue / instrument projection 一起做掉

- 优点：看起来完整
- 缺点：明显越过 `#41`

## 选型

采用方案 A。

## 设计

### 包路径

沿用当前主线布局：

- `src/perp_platform/supervisor/triggers.py`
- `tests/perp_platform/supervisor/test_triggers.py`

### 输入对象

定义 `SupervisorTriggerInputs`：

- `public_stream_lag_seconds: float`
- `private_stream_lag_seconds: float`
- `reconciliation_failed: bool`
- `repeated_recovery_failure: bool`

`repeated_recovery_failure` 先冻结成布尔信号，不在本 issue 引入计数阈值。

### 阈值常量

- `PUBLIC_DEGRADED_LAG_SECONDS = 1.5`
- `PUBLIC_RESYNC_LAG_SECONDS = 3.0`
- `PRIVATE_REDUCE_ONLY_LAG_SECONDS = 10.0`

### 求值函数

定义：

- `evaluate_supervisor_triggers(current_state, inputs) -> SupervisorTransition`

优先级从高到低：

1. `reconciliation_failed` 或 `repeated_recovery_failure`
   - 目标：`BLOCKED`
   - reason:
     - `reconciliation_failed`
     - `repeated_recovery_failure`
2. `private_stream_lag_seconds >= 10.0`
   - 目标：`REDUCE_ONLY`
   - reason: `private_stream_stale`
3. `public_stream_lag_seconds >= 3.0`
   - 目标：`RESYNCING`
   - 但若当前已在更严格状态（`REDUCE_ONLY` / `BLOCKED`），保持当前状态
   - reason:
     - `public_stream_resync_required`
     - 或当前状态保留原因
4. `public_stream_lag_seconds >= 1.5`
   - 目标：`DEGRADED`
   - 但若当前已在更严格状态（`RESYNCING` / `REDUCE_ONLY` / `BLOCKED`），保持当前状态
   - reason:
     - `public_stream_degraded`
     - 或当前状态保留原因
5. 无异常信号
   - `LIVE` / `DEGRADED` / `RESYNCING` -> 回到 `LIVE`
   - `REDUCE_ONLY` 保持 `REDUCE_ONLY`
     - reason: `cooldown_or_manual_clear_required`
   - `BLOCKED` 保持 `BLOCKED`
     - reason: `manual_unblock_required`

保持当前状态时仍通过 `transition_supervisor_state()` 走 no-op 路径。

## 测试策略

新增 `tests/perp_platform/supervisor/test_triggers.py`：

- reconciliation failure -> `BLOCKED`
- repeated recovery failure -> `BLOCKED`
- private stream stale -> `REDUCE_ONLY`
- public stream lag 3s -> `RESYNCING`
- public stream lag 1.5s -> `DEGRADED`
- healthy + `DEGRADED` -> `LIVE`
- healthy + `REDUCE_ONLY` -> `REDUCE_ONLY`
- healthy + `BLOCKED` -> `BLOCKED`

## 非目标

- 不实现 projection
- 不修改 state machine 契约
- 不引入 venue / instrument 粒度
- 不更新架构文档
