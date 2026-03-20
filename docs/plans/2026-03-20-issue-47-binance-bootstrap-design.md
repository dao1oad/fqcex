# Issue 47 Binance USD-M Runtime Bootstrap Design

## 背景

Phase 2 下一组工作是 Binance USDⓈ-M runtime。`#47` 只负责这一组里的第一步：

- 增加配置对象
- 增加 bootstrap 入口
- 固定 USDⓈ-M 的最小 endpoint 与 client label

它不能提前实现：

- public/private stream 接线
- execution path
- 配额恢复退避

## 方案比较

### 方案 A：配置对象 + bootstrap result + client target 描述

- 优点：完全符合当前 issue 的最小边界
- 优点：后续 `#48` 可以在不破坏 config 契约的前提下接入真实 client wiring
- 优点：不需要现在就引入 Binance client 类型

### 方案 B：现在就复制 Bybit 的 runtime/client wiring 结构

- 优点：形状统一
- 缺点：会把 `#48` 的实现提前带进来

### 方案 C：只加配置，不加 bootstrap

- 优点：更小
- 缺点：达不到“客户端启动入口”的交付目标

## 选型

采用方案 A。

## 设计

### 路径

- `src/perp_platform/runtime/binance/__init__.py`
- `src/perp_platform/runtime/binance/config.py`
- `src/perp_platform/runtime/binance/bootstrap.py`
- `tests/perp_platform/test_binance_runtime_bootstrap.py`

### 配置对象

定义 `BinanceRuntimeConfig`：

- `environment`
- `api_key`
- `api_secret`
- `market`
- `settle_asset`
- `rest_base_url`
- `public_ws_url`
- `private_ws_url`

冻结值：

- `market = "usdm"`
- `settle_asset = "USDT"`

允许环境：

- `testnet`
- `mainnet`

### Bootstrap 结果

定义：

- `BinanceClientTargets`
- `BinanceRuntimeBootstrapResult`

bootstrap 返回：

- `app_config`
- `runtime_config`
- `client_targets`
- `client_label`
- `private_client_enabled`

其中 `client_targets` 只描述后续 client 应连接的 endpoint，不在本 issue 中真正创建 stream/execution client。

### 默认 endpoint

`testnet`：

- `rest_base_url = https://testnet.binancefuture.com`
- `public_ws_url = wss://stream.binancefuture.com/ws`
- `private_ws_url = wss://stream.binancefuture.com/ws`

`mainnet`：

- `rest_base_url = https://fapi.binance.com`
- `public_ws_url = wss://fstream.binance.com/ws`
- `private_ws_url = wss://fstream.binance.com/ws`

### 稳定 label

- `binance-usdm-testnet`
- `binance-usdm-mainnet`

## 测试策略

新增 `tests/perp_platform/test_binance_runtime_bootstrap.py`，验证：

- config 正确读取环境变量与 endpoint override
- 非法 environment 被拒绝
- bootstrap 返回稳定 label
- bootstrap 返回固定 `market/usdm` 与 `settle_asset/USDT`
- private client 仅在 key/secret 同时存在时开启

## 非目标

- 不增加 `clients.py`
- 不增加 `runtime.py`
- 不接 public/private stream
- 不接 execution path
- 不做配额退避或恢复逻辑
