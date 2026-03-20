# Issue 49 Binance Recovery Backoff Design

## 背景

`#47/#48` 已经建立 Binance USDⓈ-M 的启动入口和 runtime wiring。`#49` 需要解决的是恢复过程中的限频敏感性：恢复不能一检测到断线就立即高频重连，而要经过可预测的 backoff。

## 方案比较

### 方案 A：单独的 recovery backoff 状态机，使用确定性的指数退避

- 优点：边界清晰，只解决恢复节流
- 优点：可直接用纯函数和测试覆盖
- 优点：后续 `#50` 冒烟测试可直接复用状态输出

### 方案 B：把 backoff 逻辑散在 runtime wiring 或 bootstrap 中

- 优点：文件少
- 缺点：职责混乱，不利于测试和后续演化

### 方案 C：先只给出常量，不建立状态机

- 优点：实现快
- 缺点：达不到“恢复退避策略”这个 issue 目标

## 选型

采用方案 A。

## 设计

### 路径

- `src/perp_platform/runtime/binance/recovery.py`
- `tests/perp_platform/binance/test_recovery_backoff.py`
- `src/perp_platform/runtime/binance/__init__.py`

### 状态机

定义：

- `BinanceRecoveryPhase`
- `BinanceRecoveryEvent`
- `BinanceRecoveryState`

最小阶段：

- `BACKING_OFF`
- `RECONNECTING`
- `PRIVATE_STREAM_RESTORED`
- `RECONCILIATION_PENDING`

最小事件：

- `BACKOFF_ELAPSED`
- `PRIVATE_STREAM_READY`
- `RESUBSCRIBE_COMPLETED`
- `RATE_LIMIT_HIT`

### 退避规则

冻结一组最小参数：

- 初始 backoff：`5` 秒
- 倍增系数：`2`
- 硬上限：`60` 秒

状态字段：

- `phase`
- `trade_mode`
- `attempt`
- `backoff_seconds`
- `subscriptions_restored`
- `reconciliation_required`

规则：

- `begin_binance_recovery()` 从 `BACKING_OFF` 开始
- `BACKOFF_ELAPSED` 才允许进入 `RECONNECTING`
- `PRIVATE_STREAM_READY` 才允许进入 `PRIVATE_STREAM_RESTORED`
- `RESUBSCRIBE_COMPLETED` 才允许进入 `RECONCILIATION_PENDING`
- 任意恢复中阶段遇到 `RATE_LIMIT_HIT`，都回到 `BACKING_OFF`，`attempt + 1`，`backoff_seconds` 按指数退避增长并封顶
- 全过程 `trade_mode` 保持 `REDUCE_ONLY`

## 测试策略

新增 `tests/perp_platform/binance/test_recovery_backoff.py`，验证：

- 初始恢复从 `BACKING_OFF` 开始
- 退避到期后才能进入重连
- 正常序列能到 `RECONCILIATION_PENDING`
- 限频事件会提高 `attempt` 并增加 `backoff_seconds`
- 退避时间在多次限频后不会超过上限

## 非目标

- 不实现真实 sleep / timer
- 不实现 listen key 生命周期
- 不实现 reconciliation 细节
- 不实现冒烟测试或端到端验证
