# Issue 44 PostgreSQL Repositories Design

## 背景

`#43` 已冻结核心 schema 和 migration。接下来 `#44` 需要把订单、仓位、余额的 canonical truth 映射到 PostgreSQL 仓储边界。

当前仓库仍然没有：

- PostgreSQL 驱动
- 连接池
- ORM

因此 `#44` 不应尝试做真实 DB 执行，而应先冻结 repository contract。

## 方案比较

### 方案 A：driver-agnostic repository，输出 SQL + params

- 优点：不引入数据库驱动
- 优点：最适合在当前阶段冻结仓储边界
- 优点：`#46` 后续可以直接拿这些语句做集成测试

### 方案 B：引入 `psycopg`，直接执行 SQL

- 优点：更像完整仓储
- 缺点：明显超出当前依赖基线

### 方案 C：只写 dataclass，不写 SQL

- 优点：实现最轻
- 缺点：不能体现“仓储”行为

## 选型

采用方案 A。

## 设计

### 路径修正

按当前主线实际布局，落点应为：

- `src/perp_platform/store/postgres/repositories/__init__.py`
- `src/perp_platform/store/postgres/repositories/base.py`
- `src/perp_platform/store/postgres/repositories/orders.py`
- `src/perp_platform/store/postgres/repositories/positions.py`
- `src/perp_platform/store/postgres/repositories/balances.py`
- `tests/perp_platform/store/test_postgres_repositories.py`

### 通用语句对象

定义 `PostgresStatement`：

- `sql`
- `params`

仓储函数/类只返回 `PostgresStatement`，不负责执行。

### Orders repository

定义：

- `OrderRecord`
- `PostgresOrdersRepository`

最小方法：

- `build_upsert(record) -> PostgresStatement`
- `build_select_for_account(venue_code, account_key) -> PostgresStatement`

`build_upsert()` 采用 `INSERT ... ON CONFLICT (venue_code, account_key, order_id) DO UPDATE`

字段映射对齐 schema：

- `venue_code`
- `account_key`
- `order_id`
- `instrument_id`
- `status`
- `order_type`
- `time_in_force`
- `reduce_only`
- `side`
- `base_qty`
- `exchange_qty`
- `exchange_qty_kind`
- `price`
- `updated_at`

### Positions repository

定义：

- `PositionRecord`
- `PostgresPositionsRepository`

最小方法：

- `build_upsert(record)`
- `build_select_for_account(venue_code, account_key)`

冲突键：

- `(venue_code, account_key, instrument_id)`

### Balances repository

定义：

- `BalanceRecord`
- `PostgresBalancesRepository`

最小方法：

- `build_upsert(record)`
- `build_select_for_account(venue_code, account_key)`

冲突键：

- `(venue_code, account_key, asset)`

### SQL 风格

- 全部使用 named params，例如 `%(venue_code)s`
- `SELECT` 默认按主键排序，保证测试可预测
- 仓储不做业务校验，只做字段映射

## 测试策略

新增 `tests/perp_platform/store/test_postgres_repositories.py`：

- orders upsert SQL 命中正确表名与 conflict key
- positions upsert SQL 命中 `base_qty/mark_price/notional_usdt`
- balances upsert SQL 命中 `wallet_balance/available_balance`
- select SQL 正确按 `venue_code/account_key` 过滤并排序
- params 字典保留输入值

## 非目标

- 不引入 DB driver
- 不执行 SQL
- 不实现 tradeability / recovery repository（留给 `#45`）
- 不写 integration test（留给 `#46`）
