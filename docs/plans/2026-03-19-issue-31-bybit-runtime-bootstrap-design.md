# Issue 31 Design

## Goal

为 `Bybit` 运行时初始化提供最小配置对象与 bootstrap 入口，不接真实网络，只证明当前主线已经具备后续 `#32` 可复用的挂点。

## Scope

- 新增 `src/perp_platform/runtime/bybit/config.py`
- 新增 `src/perp_platform/runtime/bybit/bootstrap.py`
- 新增必要的 `__init__.py`
- 新增 `tests/perp_platform/test_bybit_runtime_bootstrap.py`

## Design

- `config.py` 定义 `BybitRuntimeConfig`，通过环境变量加载最小字段。
- `bootstrap.py` 定义 `BybitRuntimeBootstrapResult`，组合全局 `AppConfig` 与 `BybitRuntimeConfig`，返回稳定 bootstrap 结果。
- 保持 CLI 现有输出契约不变，不在本 issue 引入真实客户端或真实网络连接。

## Verification

- `py -m pytest tests/perp_platform/test_bybit_runtime_bootstrap.py -q`
- `py -m pytest tests/perp_platform -q`
