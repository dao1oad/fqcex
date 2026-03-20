# Issue 36 Bybit Reconciliation Design

## 背景

`#35` 已经把 Bybit 恢复顺序建模为 `RECONCILIATION_PENDING` 终点，但当前仓库还没有“订单、仓位与余额对账”本身的最小实现。

`#36` 只负责纯本地的对账模型与 diff 结果，不提前进入 `#37` 的 `REDUCE_ONLY / BLOCKED` 投影，不调用真实交易所 API。

## 方案比较

### 方案 A：新增 `reconciliation.py`，实现快照、diff 和结果对象

- 优点：直接贴合 issue 边界
- 优点：后续 `#37` 可以直接消费 `reconciliation_passed` 与 diff 详情
- 缺点：需要先定义一组最小快照字段

### 方案 B：只在测试里比对简单字典

- 优点：实现最少
- 缺点：无法形成可复用的恢复真相对象

### 方案 C：直接做真实 venue snapshot 查询与对账

- 优点：更接近生产
- 缺点：超出当前 issue，且违反 cloud/local 边界

## 选型

采用方案 A。

## 设计

### 快照对象

新增 `src/perp_platform/runtime/bybit/reconciliation.py`：

- `BybitOrderSnapshot`
  - `order_id`
  - `status`
- `BybitPositionSnapshot`
  - `instrument_id`
  - `base_qty`
- `BybitBalanceSnapshot`
  - `asset`
  - `wallet_balance`

### 对账结果对象

- `BybitReconciliationResult`
  - `orders_match`
  - `positions_match`
  - `balances_match`
  - `passed`
  - `order_diffs`
  - `position_diffs`
  - `balance_diffs`

### 对账函数

- `reconcile_bybit_state(expected_orders, actual_orders, expected_positions, actual_positions, expected_balances, actual_balances) -> BybitReconciliationResult`

规则：

- 订单以 `order_id` 和 `status` 比较
- 仓位以 `instrument_id` 和 `base_qty` 比较
- 余额以 `asset` 和 `wallet_balance` 比较
- 比较基于集合键归一化，不依赖输入顺序
- 三类都匹配时 `passed = True`
- 任一不匹配时 `passed = False`

### 与恢复状态的接口

本 issue 不直接修改 `recovery.py` 的 phase 机，只为 `#37` 提供可消费的对账结果对象。必要时只在 `__init__.py` 导出 reconciliation 符号。

## 测试策略

新增 `tests/perp_platform/bybit/test_reconciliation.py`：

- 完整匹配时 `passed is True`
- 顺序不同但内容相同仍然通过
- 订单差异、仓位差异、余额差异分别能被识别
- 差异内容写入对应 diff 列表

## 非目标

- 不发真实查询请求
- 不做 `LIVE` / `BLOCKED` 状态投影
- 不更新 runbook
- 不处理冷却窗口
