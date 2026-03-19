# Issue 34 Bybit Smoke Tests Design

## 背景

`#31`、`#32`、`#33` 已分别完成 Bybit runtime 的 bootstrap、client wiring 和 guard 约束，但当前还缺少一个从启动到基础下单路径的 smoke 层，用于验证这些部件可以被组合成最小闭环。

`#34` 只负责“本地可验证的冒烟测试”，不建立真实网络连接，不发真实订单，不扩展到恢复流程或其他交易所。

## 方案比较

### 方案 A：只新增两个 smoke 测试文件，并在需要时补一个薄的 `order_path.py`

- 优点：最符合 issue 边界
- 优点：直接验证 bootstrap + guards + runtime wiring 的组合是否可用
- 缺点：需要新增一个很薄的 order-path 描述层

### 方案 B：把 smoke 断言继续塞进现有 `test_bybit_runtime_*` 文件

- 优点：文件更少
- 缺点：测试职责混乱，`#34` 的独立闭环不清晰

### 方案 C：做真实 mock 下单客户端或 websocket 会话

- 优点：行为更像真实系统
- 缺点：明显超出“基础下单路径冒烟测试”的最小边界

## 选型

采用方案 A。

## 设计

### 基础下单路径对象

新增 `src/perp_platform/runtime/bybit/order_path.py`：

- `BybitOrderPath`
  - `rest_base_url`
  - `category`
  - `settle_coin`
  - `order_type`
  - `time_in_force`
  - `reduce_only`
  - `private_client_required`

新增函数：

- `build_bybit_order_path(order_type, time_in_force, reduce_only, bootstrap_result) -> BybitOrderPath`

行为：

- 先调用 `validate_bybit_order_capability()`
- 用 `bootstrap_result.runtime.execution_client` 组装最小 order path
- `private_client_required` 固定为 `True`
- 不发请求、不构造签名、不建立网络连接

### Smoke 测试目录

新增目录 `tests/perp_platform/bybit/`：

- `test_bootstrap.py`
- `test_order_path.py`

### Smoke 测试内容

`test_bootstrap.py`

- 验证 bootstrap 结果同时包含：
  - `runtime.public_stream`
  - `runtime.execution_client`
  - `guards`
- 验证 private credentials 存在时 `private_client_enabled is True`

`test_order_path.py`

- 验证 `LIMIT/GTC` 与 `MARKET/IOC` 能构建基础下单路径
- 验证不允许的 `order_type` / `time_in_force` 会被拒绝
- 验证生成的 order path 继承 `rest_base_url`、`category`、`settle_coin`

## 导出边界

修改 `src/perp_platform/runtime/bybit/__init__.py`：

- 导出 `BybitOrderPath`
- 导出 `build_bybit_order_path`

## 错误处理

- 非法订单能力继续由 `validate_bybit_order_capability()` 抛 `ValueError`
- 没有 private credentials 时，允许构建 bootstrap smoke，但下单路径 smoke 应显式传入带 credentials 的 bootstrap 结果

## 测试策略

新增 `tests/perp_platform/bybit/test_bootstrap.py`

- 只验证启动 smoke 契约，不重复 `#31/#32/#33` 的所有细节

新增 `tests/perp_platform/bybit/test_order_path.py`

- 只验证最小 order path 是否能从 bootstrap 结果构建
- 重点覆盖允许/拒绝路径

## 非目标

- 不做真实下单
- 不做撤单、查询
- 不做恢复编排
- 不做账户模式变更 API
