# Issue 32 Bybit Runtime Streams Design

## 背景

`#31` 已经完成了 Bybit runtime 的配置加载与 bootstrap 入口，但当前返回值只有稳定标签与私有客户端开关，还没有把公共流、私有流和执行客户端收口成可复用的 runtime wiring 对象。

`#32` 只负责把这些入口接通为可构造、可测试的最小运行时描述，不直接建立真实网络连接，不提前实现 `#33` 的能力约束，不扩大到其他交易所。

## 方案比较

### 方案 A：在 `bootstrap.py` 里继续堆字符串字段

- 优点：改动最少
- 缺点：公共流、私有流和执行客户端仍然没有统一对象边界，后续 issue 会很快返工

### 方案 B：新增 `clients.py`，并用 `runtime.py` 组装 runtime wiring

- 优点：把三类客户端抽象成稳定值对象，后续 `#33+` 可以直接复用
- 优点：不触发真实连接，不突破当前 issue 边界
- 缺点：会新增一个轻量 wiring 层

### 方案 C：直接做真实 Bybit runtime / websocket / execution adapter

- 优点：功能最完整
- 缺点：明显越过 `#32` 边界，提前进入真实 IO、恢复和能力约束

## 选型

采用方案 B。

## 设计

### 数据对象

新增 `src/perp_platform/runtime/bybit/clients.py`：

- `BybitStreamClient`
  - `channel`: `public` / `private`
  - `url`
  - `category`
  - `requires_auth`
- `BybitExecutionClient`
  - `rest_base_url`
  - `category`
  - `settle_coin`
  - `api_key_present`
  - `api_secret_present`

### Wiring 层

新增 `src/perp_platform/runtime/bybit/runtime.py`：

- `BybitRuntimeWiring`
  - `public_stream`
  - `private_stream`
  - `execution_client`
- `wire_bybit_runtime(config: BybitRuntimeConfig) -> BybitRuntimeWiring`

规则：

- `public_stream` 总是存在
- `private_stream` 只有在 `api_key` 与 `api_secret` 同时存在时才创建
- `execution_client` 总是存在，但只暴露配置真相，不建立真实连接

### Bootstrap 接口

修改 `src/perp_platform/runtime/bybit/bootstrap.py`：

- `BybitRuntimeBootstrapResult` 增加 `runtime`
- `bootstrap_bybit_runtime()` 内部调用 `wire_bybit_runtime()`
- 保留现有 `client_label` 与 `private_client_enabled`，避免破坏 `#31` 既有测试契约

### 导出边界

修改 `src/perp_platform/runtime/bybit/__init__.py`：

- 导出 `BybitStreamClient`
- 导出 `BybitExecutionClient`
- 导出 `BybitRuntimeWiring`
- 导出 `wire_bybit_runtime`

## 错误处理

- 不新增新的外部依赖
- 不建立真实网络连接，因此不引入 IO 异常分支
- 私有客户端缺少凭证时，返回 `None`，而不是隐式伪造鉴权客户端

## 测试策略

新增 `tests/perp_platform/test_bybit_runtime_clients.py`：

- `wire_bybit_runtime()` 在无私钥时只返回 `public_stream` 与 `execution_client`
- `wire_bybit_runtime()` 在有私钥时返回 `private_stream`
- `execution_client` 正确继承 `rest_base_url`、`category`、`settle_coin`

更新 `tests/perp_platform/test_bybit_runtime_bootstrap.py`：

- `bootstrap_bybit_runtime()` 返回的 `runtime` 包含 wiring 对象
- 现有 `client_label` / `private_client_enabled` 行为保持稳定

## 非目标

- 不连接真实 websocket
- 不实现执行请求发送
- 不增加 `#33` 的 `one_way` / `isolated` / 订单能力约束
- 不修改 Phase 1 边界文档
