# Issue 53 OKX Runtime Guards Design

## 背景

`#51` 已经提供 OKX runtime bootstrap，`#52` 已经提供张数换算 wrapper。`#53` 只补齐剩余的 venue 约束：

- OKX 单向持仓约束
- `isolated` 交易模式约束
- Phase 1 允许的下单能力约束

这个 issue 不做：

- recovery
- smoke / regression test 汇总
- 新的 clients 模块

## 方案比较

### 方案 A：guards 模块 + 最小 runtime wiring + bootstrap 集成

- 优点：与 Bybit 当前结构接近
- 优点：约束集中在 OKX runtime 边界层
- 优点：为 `#54` 回归测试提供稳定入口

### 方案 B：只在未来调用点分散校验

- 优点：短期代码更少
- 缺点：下单路径约束会散落
- 缺点：bootstrap 无法直接返回 Phase 1 安全边界

### 方案 C：直接扩成完整 native order adapter

- 优点：看起来更完整
- 缺点：明显超出 Phase 2 当前 issue 边界

## 选型

采用方案 A。

## 设计

### 路径

- `src/perp_platform/runtime/okx/guards.py`
- `src/perp_platform/runtime/okx/runtime.py`
- `src/perp_platform/runtime/okx/bootstrap.py`
- `src/perp_platform/runtime/okx/__init__.py`
- `tests/perp_platform/test_okx_guards.py`
- `tests/perp_platform/test_okx_runtime_bootstrap.py`

### 持仓与保证金约束

定义 `OkxRuntimeGuards`：

- `position_mode = "net"`
- `margin_mode = "isolated"`
- `default_leverage = 2`
- `max_leverage = 3`
- `allowed_order_types = ("LIMIT", "MARKET")`
- `allowed_time_in_force = ("GTC", "IOC")`
- `reduce_only_supported = True`

这里使用 OKX 官方边界口径：

- `net` 是 OKX 的单向持仓等价模式
- `isolated` 直接对应 OKX `tdMode`

### 下单能力约束

新增：

- `build_okx_runtime_guards()`
- `validate_okx_leverage(...)`
- `validate_okx_order_capability(...)`

组合规则：

- `LIMIT + GTC` 允许
- `LIMIT + IOC` 允许
- `MARKET + IOC` 允许
- `MARKET + GTC` 拒绝

这样既保持 Phase 1 的统一表述，又不伪造 OKX 不存在的长期挂单 market 语义。

### 最小 runtime wiring

定义 `OkxRuntimeWiring`：

- `rest_base_url`
- `public_ws_url`
- `private_ws_url`
- `instrument_type`
- `settle_asset`
- `position_mode`
- `margin_mode`

`wire_okx_runtime(config, guards)` 负责把 bootstrap config 和 guard 边界收口为一个稳定运行时对象：

- private credentials 不完整时，`private_ws_url = None`
- `position_mode` 与 `margin_mode` 从 guards 投影而来

### Bootstrap 集成

`bootstrap_okx_runtime(...)` 追加返回：

- `runtime`
- `guards`

保留现有：

- `client_label`
- `private_client_enabled`

## 测试策略

新增 `tests/perp_platform/test_okx_guards.py`，验证：

- Phase 1 guard 值稳定
- leverage 上下界约束正确
- order capability 允许与拒绝组合正确

更新 `tests/perp_platform/test_okx_runtime_bootstrap.py`，验证：

- bootstrap 结果包含 `runtime` 和 `guards`
- `runtime.position_mode == "net"`
- `runtime.margin_mode == "isolated"`
- private credentials 不完整时 private 路径关闭

## 非目标

- 不新增 `clients.py`
- 不新增 recovery 状态机
- 不实现回归测试聚合
- 不实现下单执行器
