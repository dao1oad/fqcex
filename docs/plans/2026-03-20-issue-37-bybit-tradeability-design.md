# Issue 37 Bybit Tradeability Projection Design

## 背景

`#35` 已定义恢复顺序，`#36` 已定义订单、仓位、余额的对账结果，但当前还没有把这两类输入投影成 `REDUCE_ONLY` 或 `BLOCKED` 的最小 tradeability 真相。

`#37` 只负责做投影层，不负责 runbook 文字补充，也不把状态恢复到 `LIVE`。`LIVE` 的回归条件和操作员说明继续留给后续文档与场景测试。

## 方案比较

### 方案 A：新增 `tradeability.py`，定义 projection 模式、原因和 blocker 列表

- 优点：边界清晰，正好消费 `#35` 和 `#36`
- 优点：后续 `#38` 可直接围绕这些投影结果补场景测试与 runbook
- 缺点：需要先冻结一组最小 reason label

### 方案 B：直接在 recovery 或 reconciliation 模块里返回 tradeability

- 优点：文件更少
- 缺点：把顺序、对账、投影三种职责混在一起，不利于后续扩展

### 方案 C：直接引入 `LIVE`

- 优点：看起来更完整
- 缺点：已经超出 issue 标题。当前 issue 只要求投影 `REDUCE_ONLY` 与 `BLOCKED`

## 选型

采用方案 A。

## 设计

### 投影对象

新增 `src/perp_platform/runtime/bybit/tradeability.py`：

- `BybitTradeabilityMode`
  - `REDUCE_ONLY`
  - `BLOCKED`
- `BybitTradeabilityProjection`
  - `mode`
  - `reason`
  - `blockers`

### 投影函数

- `project_bybit_tradeability(recovery_state, reconciliation_result | None) -> BybitTradeabilityProjection`

规则：

- 如果恢复阶段尚未走到 `RECONCILIATION_PENDING`
  - 返回 `REDUCE_ONLY`
  - `reason = "recovery_in_progress"`
- 如果已到 `RECONCILIATION_PENDING`，但还没有对账结果
  - 返回 `REDUCE_ONLY`
  - `reason = "reconciliation_pending"`
- 如果对账结果 `passed = False`
  - 返回 `BLOCKED`
  - `reason = "reconciliation_failed"`
  - `blockers` 收集 `order_diffs` / `position_diffs` / `balance_diffs`
- 如果对账结果 `passed = True`
  - 返回 `REDUCE_ONLY`
  - `reason = "cooldown_pending"`
  - `blockers = []`

这与现有文档一致：
- 恢复阶段默认 `REDUCE_ONLY`
- 对账失败进入 `BLOCKED`
- 回到 `LIVE` 还需要额外 cooldown / anomaly 观察，不在本 issue 内

### 导出边界

修改 `src/perp_platform/runtime/bybit/__init__.py`：

- 导出 `BybitTradeabilityMode`
- 导出 `BybitTradeabilityProjection`
- 导出 `project_bybit_tradeability`

## 测试策略

新增 `tests/perp_platform/bybit/test_tradeability_projection.py`：

- 恢复中返回 `REDUCE_ONLY`
- 等待对账返回 `REDUCE_ONLY`
- 对账失败返回 `BLOCKED` 且 blocker 列表非空
- 对账通过后仍返回 `REDUCE_ONLY`，原因是 `cooldown_pending`

## 非目标

- 不把状态恢复到 `LIVE`
- 不新增 runbook 说明
- 不做操作员 override 流程
