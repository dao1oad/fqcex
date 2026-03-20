# Issue 51 OKX Swap Runtime Bootstrap Design

## 背景

Phase 2 最后一组 venue 是 OKX。`#51` 只负责第一步：

- 增加 USDT 永续（`SWAP`）配置
- 增加 bootstrap 入口
- 固定 demo/mainnet endpoint 与稳定 client label

它不提前实现：

- 张数换算
- 下单路径与单向/逐仓约束
- 启动回归测试

## 方案比较

### 方案 A：配置对象 + bootstrap result + client target 描述

- 优点：与 `#47` Binance 的分层一致
- 优点：为 `#52/#53` 留出稳定入口
- 优点：当前只解决 config/bootstrap 边界

### 方案 B：立即引入完整 clients/runtime wiring

- 优点：形状一次到位
- 缺点：会把 `#52/#53` 的范围提前带进来

### 方案 C：只加 config，不加 bootstrap

- 优点：更小
- 缺点：达不到启动入口目标

## 选型

采用方案 A。

## 设计

### 路径

- `src/perp_platform/runtime/okx/__init__.py`
- `src/perp_platform/runtime/okx/config.py`
- `src/perp_platform/runtime/okx/bootstrap.py`
- `tests/perp_platform/test_okx_runtime_bootstrap.py`

### 配置对象

定义 `OkxRuntimeConfig`：

- `environment`
- `api_key`
- `api_secret`
- `api_passphrase`
- `instrument_type`
- `settle_asset`
- `rest_base_url`
- `public_ws_url`
- `private_ws_url`

冻结值：

- `instrument_type = "SWAP"`
- `settle_asset = "USDT"`

允许环境：

- `demo`
- `mainnet`

### 默认 endpoint

依据 OKX 官方 API guide：

- Production Trading:
  - REST: `https://www.okx.com`
  - Public WebSocket: `wss://ws.okx.com:8443/ws/v5/public`
  - Private WebSocket: `wss://ws.okx.com:8443/ws/v5/private`
- Demo Trading:
  - REST: `https://www.okx.com`
  - Public WebSocket: `wss://wspap.okx.com:8443/ws/v5/public`
  - Private WebSocket: `wss://wspap.okx.com:8443/ws/v5/private`

这里把环境名收口为 `demo`，不自行发明 `testnet` 别名。

### Bootstrap 结果

定义：

- `OkxClientTargets`
- `OkxRuntimeBootstrapResult`

bootstrap 返回：

- `app_config`
- `runtime_config`
- `client_targets`
- `client_label`
- `private_client_enabled`

`private_client_enabled` 需要 key/secret/passphrase 同时存在才为真。

### 稳定 label

- `okx-swap-demo`
- `okx-swap-mainnet`

## 测试策略

新增 `tests/perp_platform/test_okx_runtime_bootstrap.py`，验证：

- config 正确读取环境变量与 endpoint override
- 非法 environment 被拒绝
- bootstrap 返回稳定 label
- `instrument_type/SWAP` 与 `settle_asset/USDT` 冻结
- private client 仅在三段凭证同时存在时开启

## 非目标

- 不增加 `clients.py`
- 不增加 `runtime.py`
- 不做张数换算
- 不做单向/逐仓约束
