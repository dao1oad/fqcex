# Issue 48 Binance Runtime Streams And Execution Design

## 背景

`#47` 已建立 Binance USDⓈ-M 的 config 与 bootstrap 入口。`#48` 需要在不引入恢复/退避逻辑的前提下，把 runtime 接到最小的三条路径：

- public stream
- private stream
- execution path

## 方案比较

### 方案 A：沿用 Bybit 的 client dataclass + runtime wiring 形状

- 优点：与现有 venue runtime 结构一致
- 优点：后续 `#49/#50` 可直接复用
- 优点：仍然是纯对象 wiring，不引入真实网络客户端

### 方案 B：直接在 `bootstrap.py` 里内联所有 client dataclass

- 优点：文件更少
- 缺点：会把 bootstrap 变成新旧职责混合点，不利于 `#49` 继续演化

### 方案 C：只补 execution path，不接 private/public

- 优点：实现更快
- 缺点：不满足 issue 目标

## 选型

采用方案 A。

## 设计

### 路径

- `src/perp_platform/runtime/binance/clients.py`
- `src/perp_platform/runtime/binance/runtime.py`
- `src/perp_platform/runtime/binance/bootstrap.py`
- `src/perp_platform/runtime/binance/__init__.py`
- `tests/perp_platform/test_binance_runtime_clients.py`
- `tests/perp_platform/test_binance_runtime_bootstrap.py`

### Client dataclass

定义：

- `BinanceStreamClient`
- `BinanceExecutionClient`

字段口径：

- stream:
  - `channel`
  - `url`
  - `market`
  - `requires_auth`
- execution:
  - `rest_base_url`
  - `market`
  - `settle_asset`
  - `api_key_present`
  - `api_secret_present`

### Runtime wiring

定义：

- `BinanceRuntimeWiring`
- `wire_binance_runtime(config)`

规则：

- 始终创建 public stream
- 只有 key/secret 同时存在时才创建 private stream
- execution client 始终存在，但只记录 credential presence

### Bootstrap 扩展

在不破坏 `#47` 现有字段的前提下，为 `BinanceRuntimeBootstrapResult` 增加：

- `runtime`

这样 `#47` 的 config/label 语义保持稳定，而 `#48` 把真正的 wiring 挂接到 bootstrap 结果上。

## 测试策略

新增 `tests/perp_platform/test_binance_runtime_clients.py`：

- 无 credentials 时 private stream 为 `None`
- 有 credentials 时 private stream 开启
- execution client 保持 market / settle_asset / credential flags

更新 `tests/perp_platform/test_binance_runtime_bootstrap.py`：

- bootstrap result 暴露 `runtime`
- runtime.public_stream / execution_client endpoint 与 config 一致

## 非目标

- 不引入 listen key 生命周期
- 不实现配额退避
- 不实现恢复状态机
- 不接真实 websocket/rest SDK
