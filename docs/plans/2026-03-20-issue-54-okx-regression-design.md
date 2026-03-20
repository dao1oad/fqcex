# Issue 54 OKX Runtime Regression Test Design

## 背景

OKX 这一组 child issue 到 `#53` 为止已经具备：

- bootstrap/config
- contracts -> `base_qty` conversion
- runtime guards 与最小 wiring

`#54` 只做最后一层回归测试，把这些能力从使用者视角串起来，避免后续重构把 OKX runtime 公开边界打散。

## 方案比较

### 方案 A：在 `tests/perp_platform/okx` 下增加 package 级回归测试

- 优点：和 Binance / Bybit 的 venue test package 结构一致
- 优点：覆盖 package export、bootstrap、conversion、guards 的联合行为
- 优点：不需要再改生产代码

### 方案 B：继续往现有顶层 `test_okx_runtime_bootstrap.py` / `test_conversion.py` 里追加断言

- 优点：文件更少
- 缺点：缺少 venue package 视角的回归分层
- 缺点：后续查看 OKX 专项回归时不集中

### 方案 C：引入 smoke 脚本或集成测试 runner

- 优点：更接近真实流程
- 缺点：超出当前 issue 边界

## 选型

采用方案 A。

## 设计

### 路径

- `tests/perp_platform/okx/test_bootstrap.py`
- `tests/perp_platform/okx/test_runtime_regression.py`

`tests/perp_platform/okx/__init__.py` 已在 `#52` 创建，这里直接复用。

### 回归覆盖面

`test_bootstrap.py` 负责：

- 通过 package 顶层 `perp_platform.runtime.okx` 导入公开 API
- 校验 bootstrap 结果中的 runtime/guards/client label 保持稳定
- 校验 private credentials 缺失时 private 路径仍关闭

`test_runtime_regression.py` 负责：

- 校验 conversion helper 通过 package 顶层导出可用
- 校验 `contracts -> base_qty` 与 guards/runtime 的联合行为
- 校验 `LIMIT/GTC` 与 `MARKET/IOC` 在 bootstrap 结果 guards 下仍可通过
- 校验 `MARKET/GTC` 仍被拒绝

### 边界

- 不修改生产代码
- 不改变现有顶层 unit test 契约
- 不扩展到 recovery / client / execution 流程

## 测试策略

新增：

- `tests/perp_platform/okx/test_bootstrap.py`
- `tests/perp_platform/okx/test_runtime_regression.py`

并继续执行：

- `py -m pytest tests/perp_platform/okx -q`
- `py -m pytest tests/perp_platform -q`
- `py -m pytest tests -q`

## 非目标

- 不新增 OKX smoke 脚本
- 不新增真实 API 调用
- 不新增运行时实现
