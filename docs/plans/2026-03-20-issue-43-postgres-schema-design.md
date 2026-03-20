# Issue 43 PostgreSQL Core Schema Design

## 背景

Phase 2 的 tracking `#15` 需要先冻结 PostgreSQL 真相存储的核心 schema，后续 `#44/#45` 再分别补订单/仓位/余额仓储，以及可交易性/恢复持久化。

当前仓库还没有：

- 数据库驱动依赖
- ORM / migration 框架
- `store/postgres` 包结构

因此 `#43` 只做最小可落地基座：

- 初始 SQL migration
- Python 侧的 schema 常量与表名定义
- 针对 migration / schema 的契约测试

## 方案比较

### 方案 A：纯 SQL migration + Python schema 常量模块

- 优点：依赖最少
- 优点：最符合 `#43` “核心 Schema 与迁移”的边界
- 优点：不把 ORM / driver / connection 管理偷渡进来

### 方案 B：直接引入 Alembic / SQLAlchemy

- 优点：后续迁移体验更完整
- 缺点：当前仓库没有依赖基线；这一跳会把 `#43` 变成工具链引入 issue

### 方案 C：只写 Python 常量，不落 migration 文件

- 优点：实现最轻
- 缺点：不满足 issue 对“迁移”的要求

## 选型

采用方案 A。

## 设计

### 路径修正

issue 正文里的 `apps/...` 是旧路径，当前主线实际落点应为：

- `migrations/postgres/0001_core_truth_schema.sql`
- `src/perp_platform/store/__init__.py`
- `src/perp_platform/store/postgres/__init__.py`
- `src/perp_platform/store/postgres/schema.py`
- `tests/perp_platform/store/test_postgres_schema.py`

### 初始核心表

基于 `docs/architecture/DATA_MODEL.md` 的 minimum truth store tables，`#43` 冻结以下 9 张表：

- `venues`
- `accounts`
- `instruments`
- `connection_states`
- `tradeability_states`
- `recovery_runs`
- `orders`
- `positions`
- `balances`

### 表字段范围

#### 1. `venues`

- `venue_code` `TEXT PRIMARY KEY`
- `created_at` `TIMESTAMPTZ`

#### 2. `accounts`

- `account_key` `TEXT PRIMARY KEY`
- `venue_code` `TEXT REFERENCES venues(venue_code)`
- `account_label` `TEXT`
- `created_at` `TIMESTAMPTZ`

#### 3. `instruments`

- `instrument_id` `TEXT PRIMARY KEY`
- `base_asset` `TEXT`
- `quote_asset` `TEXT`
- `kind` `TEXT`
- `created_at` `TIMESTAMPTZ`

#### 4. `connection_states`

- `venue_code`
- `account_key`
- `stream_type`
- `status`
- `detail_reason`
- `observed_at`
- 主键：`(venue_code, account_key, stream_type)`

#### 5. `tradeability_states`

- `scope_type`
- `venue_code`
- `account_key`
- `instrument_id`
- `supervisor_state`
- `allow_open`
- `allow_reduce`
- `reason`
- `updated_at`
- 唯一键：`(scope_type, venue_code, account_key, instrument_id)`

其中 venue 级 scope 约定 `instrument_id = ''`，避免 nullable key 让唯一约束复杂化。

#### 6. `recovery_runs`

- `recovery_run_id` `BIGSERIAL PRIMARY KEY`
- `venue_code`
- `account_key`
- `phase`
- `status`
- `trigger_reason`
- `blockers_json` `JSONB`
- `started_at`
- `completed_at`

#### 7. `orders`

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
- 主键：`(venue_code, account_key, order_id)`

#### 8. `positions`

- `venue_code`
- `account_key`
- `instrument_id`
- `base_qty`
- `mark_price`
- `notional_usdt`
- `position_mode`
- `margin_mode`
- `leverage`
- `updated_at`
- 主键：`(venue_code, account_key, instrument_id)`

#### 9. `balances`

- `venue_code`
- `account_key`
- `asset`
- `wallet_balance`
- `available_balance`
- `updated_at`
- 主键：`(venue_code, account_key, asset)`

### 数据类型策略

- 数量与价格先统一使用 `NUMERIC(36, 18)`，与后续仓储实现兼容
- `exchange_qty` / `exchange_qty_kind` 作为 edge-only 存档字段保留
- `blockers_json` 使用 `JSONB`
- 时间统一 `TIMESTAMPTZ`

### Python schema 模块

`src/perp_platform/store/postgres/schema.py` 提供：

- 表名常量
- `CORE_TRUTH_TABLES`
- `CORE_SCHEMA_VERSION = "0001"`
- `CORE_SCHEMA_SQL`（与 migration 文件口径一致）

这里不实现 DB 连接和执行器，只提供 schema 契约。

## 测试策略

新增 `tests/perp_platform/store/test_postgres_schema.py`：

- Python schema 模块可导入
- `CORE_TRUTH_TABLES` 包含 9 张表
- migration 文件存在且包含这些表定义
- 关键字段名存在：
  - `base_qty`
  - `mark_price`
  - `notional_usdt`
  - `supervisor_state`
  - `blockers_json`

## 非目标

- 不引入 Alembic / SQLAlchemy / psycopg
- 不实现 repository
- 不做 DB integration test
- 不写初始化 runbook（留给 `#46`）
