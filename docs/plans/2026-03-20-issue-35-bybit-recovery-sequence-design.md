# Issue 35 Bybit Recovery Sequence Design

## 背景

Bybit runtime 初始化与启动 smoke 已完成，但恢复闭环还没有最基本的“重连与重订阅顺序”模型。当前仓库里只有 runbook 描述，还没有可测试的恢复顺序代码边界。

`#35` 只负责把恢复顺序编码成最小状态机/步骤推进器，不提前进入 `#36` 的订单、仓位、余额对账，也不提前进入 `#37` 的 `REDUCE_ONLY / BLOCKED` 投影。

## 方案比较

### 方案 A：新增 `recovery.py`，定义 phase、event 和推进函数

- 优点：边界清晰、纯本地、测试简单
- 优点：后续 `#36/#37` 可以直接复用恢复阶段真相
- 缺点：需要先冻结一组最小 phase 名称

### 方案 B：只在测试里写顺序断言，不写实现对象

- 优点：实现最少
- 缺点：恢复顺序无法被后续代码复用，只是测试常量

### 方案 C：直接做完整恢复状态机

- 优点：一步到位
- 缺点：明显超出 `#35` 范围，会把对账和 tradeability 投影一起拖进来

## 选型

采用方案 A。

## 设计

### 恢复阶段

新增 `src/perp_platform/runtime/bybit/recovery.py`：

- `BybitRecoveryPhase`
  - `DISCONNECTED`
  - `RECONNECTING`
  - `PRIVATE_STREAM_RESTORED`
  - `RESUBSCRIBED`
  - `RECONCILIATION_PENDING`

### 恢复事件

- `BybitRecoveryEvent`
  - `RECONNECT_STARTED`
  - `PRIVATE_STREAM_READY`
  - `RESUBSCRIBE_COMPLETED`

### 恢复状态对象

- `BybitRecoveryState`
  - `phase`
  - `trade_mode`: 固定为恢复阶段的 `REDUCE_ONLY`
  - `subscriptions_restored`
  - `reconciliation_required`

### 推进函数

- `begin_bybit_recovery() -> BybitRecoveryState`
- `advance_bybit_recovery(state, event) -> BybitRecoveryState`

规则：

- `begin_bybit_recovery()` 直接返回 `RECONNECTING`
- 只有收到 `PRIVATE_STREAM_READY` 才能进入 `PRIVATE_STREAM_RESTORED`
- 只有在 `PRIVATE_STREAM_RESTORED` 后收到 `RESUBSCRIBE_COMPLETED` 才能进入 `RECONCILIATION_PENDING`
- 所有恢复阶段默认 `trade_mode = "REDUCE_ONLY"`
- 不允许跳步；非法顺序抛 `ValueError`

## 测试策略

新增 `tests/perp_platform/bybit/test_recovery_sequence.py`：

- `begin_bybit_recovery()` 返回 `RECONNECTING`
- 正常顺序推进：
  - `RECONNECT_STARTED` 已隐含在 begin
  - `PRIVATE_STREAM_READY`
  - `RESUBSCRIBE_COMPLETED`
  - 最终进入 `RECONCILIATION_PENDING`
- 非法顺序：
  - 未恢复私有流前就 `RESUBSCRIBE_COMPLETED`
  - 在终态继续推进
- 所有状态都维持 `trade_mode == "REDUCE_ONLY"`

## 导出边界

修改 `src/perp_platform/runtime/bybit/__init__.py`：

- 导出 recovery phase / event / state / helper 函数

## 非目标

- 不做订单、仓位、余额对账
- 不做 `BLOCKED` 投影
- 不接真实 websocket
- 不更新 runbook
