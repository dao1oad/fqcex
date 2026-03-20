# Issue 50 Binance Smoke And Recovery Consistency Tests Design

## 背景

`#47/#48/#49` 已经依次完成：

- config 与 bootstrap
- public/private/execution wiring
- recovery backoff

`#50` 不再增加生产能力，只负责把这一组最小闭环变成可回归的 smoke 与 consistency tests。

## 方案比较

### 方案 A：只增加两组测试，不改生产代码

- 优点：完全符合本 issue 的边界
- 优点：可以把当前 Binance runtime 契约冻结下来
- 优点：合并后即可作为后续 venue 回归的 smoke 基线

### 方案 B：顺手调整 recovery 或 bootstrap 结构

- 优点：可以顺便“优化”接口
- 缺点：超出本 issue，且没有必要

### 方案 C：只测 bootstrap，不测 recovery consistency

- 优点：实现更快
- 缺点：不能证明恢复阶段的一致性约束

## 选型

采用方案 A。

## 设计

### 路径

- `tests/perp_platform/binance/test_bootstrap.py`
- `tests/perp_platform/binance/test_recovery_consistency.py`

### Bootstrap smoke tests

覆盖：

- `bootstrap_binance_runtime()` 在 testnet/mainnet 都能给出稳定结果
- runtime wiring、client label、private credential gate 一致
- `client_targets` 与 `runtime` 中的 endpoint 一致

### Recovery consistency tests

覆盖：

- 恢复在 `BACKING_OFF` / `RECONNECTING` / `PRIVATE_STREAM_RESTORED` 阶段都保持 `REDUCE_ONLY`
- 正常序列结束后进入 `RECONCILIATION_PENDING`，并要求对账
- 任何恢复中阶段如果命中 `RATE_LIMIT_HIT`，都会回到 `BACKING_OFF` 并清空订阅恢复状态

## 测试策略

定向：

- `py -m pytest tests/perp_platform/binance -q`

回归：

- `py -m pytest tests/perp_platform -q`
- `py -m pytest tests -q`

## 非目标

- 不增加生产代码
- 不引入网络 smoke
- 不做 listen key 生命周期测试
- 不做跨交易所对比测试
