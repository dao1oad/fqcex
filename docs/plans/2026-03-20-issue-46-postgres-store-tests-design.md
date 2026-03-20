# Issue 46 PostgreSQL Store Integration Tests And Initialization Docs Design

## 背景

`#43` 到 `#45` 已经分别完成：

- 核心 schema 与迁移
- orders / positions / balances repository
- tradeability / recovery repository

当前还缺一层更高的 store contract，用来证明 schema、repository builder、canonical truth fields 与初始化文档在同一个持久化边界内保持一致。

## 方案比较

### 方案 A：增加高层 contract test，并补 DATA_MODEL 中的持久化说明

- 优点：完全符合当前 issue 的预期文件
- 优点：不引入真实数据库依赖
- 优点：可以直接验证 schema、repository、canonical 字段、初始化路径是否一致

### 方案 B：增加真实 PostgreSQL integration test

- 优点：更贴近最终运行
- 缺点：需要数据库环境与执行层，超出当前 issue 边界

### 方案 C：只补文档，不补高层测试

- 优点：实现最快
- 缺点：不能形成自动化验收信号

## 选型

采用方案 A。

## 设计

### 路径

- `tests/perp_platform/store/test_postgres_store.py`
- `docs/architecture/DATA_MODEL.md`

### Store contract test

新增一组高层测试，验证：

- schema 导出的 `CORE_TRUTH_TABLES` 与各 repository 覆盖范围一致
- `orders` / `positions` / `balances` / `tradeability_states` / `recovery_runs` 五类真相写入边界都可被 builder contract 命中
- canonical fields `base_qty`、`mark_price`、`notional_usdt`、`supervisor_state`、`blockers_json` 同时出现在 schema / repository contract 中
- store package 的初始化入口能够暴露 PostgreSQL schema 与 repository symbols

测试继续使用 driver-agnostic 方式：

- 不连接数据库
- 不引入执行器
- 只验证 SQL contract、symbols 和字段映射

### DATA_MODEL 文档补充

在 `DATA_MODEL.md` 追加 `Truth Store Initialization` 与 `Persistence Mapping` 两节，明确：

- PostgreSQL truth store 当前的初始化入口是迁移文件 `migrations/postgres/0001_core_truth_schema.sql`
- `CORE_TRUTH_TABLES` 是最小初始化表集
- `orders`、`positions`、`balances`、`tradeability_states`、`recovery_runs` 分别承载哪类真相
- canonical fields 如何映射到持久化层：
  - `base_qty`
  - `mark_price`
  - `notional_usdt`
  - `supervisor_state`
  - `blockers_json`

## 测试策略

定向验证：

- `py -m pytest tests/perp_platform/store/test_postgres_store.py -q`

本 issue 指定验证：

- `py -m pytest tests/perp_platform/store -q`

回归验证：

- `py -m pytest tests -q`

## 非目标

- 不增加真实 PostgreSQL integration environment
- 不新增 DB 执行器
- 不修改 schema 结构
- 不扩展到 Binance / OKX runtime
