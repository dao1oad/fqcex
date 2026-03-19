# Issue 33 Bybit Guards Design

## 背景

`#32` 已经为 Bybit runtime 接通了公共流、私有流和执行客户端的 wiring，但当前 runtime 仍未把 Phase 1 冻结的交易约束编码为可测试的运行时 guard。

`#33` 只负责把这些约束收口成声明式 guard 与校验函数，不触发真实 Bybit 账户设置 API，不提前实现冒烟下单或恢复流程。

## 方案比较

### 方案 A：新增 `guards.py`，把约束建模成稳定值对象并提供校验函数

- 优点：边界清晰，测试成本低
- 优点：后续下单路径和 smoke test 可以直接复用
- 缺点：需要在 bootstrap 上多暴露一个 guard 字段

### 方案 B：把约束直接散落在 `runtime.py` 或 future order path 中

- 优点：当前改动看起来更少
- 缺点：规则分散，后续很快会重复实现和返工

### 方案 C：直接做真实 Bybit 模式设置与拦截

- 优点：最接近生产行为
- 缺点：明显超出 `#33`，提前进入真实交易 API 和恢复边界

## 选型

采用方案 A。

## 设计

### 数据对象

新增 `src/perp_platform/runtime/bybit/guards.py`：

- `BybitRuntimeGuards`
  - `position_mode`: 固定 `one_way`
  - `margin_mode`: 固定 `isolated`
  - `default_leverage`: 固定 `2`
  - `max_leverage`: 固定 `3`
  - `allowed_order_types`: `LIMIT` / `MARKET`
  - `allowed_time_in_force`: `GTC` / `IOC`
  - `reduce_only_supported`: `True`

### 行为函数

新增：

- `build_bybit_runtime_guards() -> BybitRuntimeGuards`
- `validate_bybit_leverage(leverage: int, guards: BybitRuntimeGuards) -> None`
- `validate_bybit_order_capability(order_type: str, time_in_force: str, reduce_only: bool, guards: BybitRuntimeGuards) -> None`

约束：

- leverage 必须 `>= 1` 且 `<= max_leverage`
- `default_leverage` 只是默认值，不强制所有请求都等于 `2`
- `order_type` 仅允许 `LIMIT` / `MARKET`
- `time_in_force` 仅允许 `GTC` / `IOC`
- `reduce_only=False` 仍然允许，只是显式表明 `reduce_only` 能力受支持

### Bootstrap 暴露

修改 `src/perp_platform/runtime/bybit/bootstrap.py`：

- `BybitRuntimeBootstrapResult` 增加 `guards`
- `bootstrap_bybit_runtime()` 调用 `build_bybit_runtime_guards()`

这样后续 `#34` smoke test 或更后面的下单入口，可以直接从 bootstrap 产物读取 guard 约束。

### 导出边界

修改 `src/perp_platform/runtime/bybit/__init__.py`：

- 导出 `BybitRuntimeGuards`
- 导出 `build_bybit_runtime_guards`
- 导出两个 validate 函数

## 错误处理

- 对非法 leverage 抛 `ValueError`
- 对非法 `order_type` / `time_in_force` 抛 `ValueError`
- 暂不处理真实账户状态不一致，因为当前 issue 不涉及真实 API

## 测试策略

新增 `tests/perp_platform/test_bybit_guards.py`：

- `build_bybit_runtime_guards()` 返回冻结的 Phase 1 约束
- leverage `2` 与 `3` 通过，`4` 失败
- `LIMIT/GTC` 与 `MARKET/IOC` 通过
- 非法订单类型或非法 `time_in_force` 失败

更新 `tests/perp_platform/test_bybit_runtime_bootstrap.py`：

- bootstrap 结果包含 `guards`
- `guards.position_mode == "one_way"`
- `guards.margin_mode == "isolated"`

## 非目标

- 不调用真实 Bybit 设置接口
- 不做仓位模式切换流程
- 不做真实下单 / 撤单
- 不扩展到 Binance / OKX
