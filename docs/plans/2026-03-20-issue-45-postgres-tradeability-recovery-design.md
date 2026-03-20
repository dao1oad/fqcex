# Issue 45 PostgreSQL Tradeability And Recovery Repositories Design

## 背景

`#43` 已建立核心 schema，`#44` 已为 orders / positions / balances 建立 driver-agnostic repository contract。`#45` 需要补齐剩余两类状态：

- `tradeability_states`
- `recovery_runs`

这两类数据直接对应 Supervisor 状态与恢复流程，是后续 runtime / operator 观察的关键持久化边界。

## 方案比较

### 方案 A：继续沿用 statement builder contract

- 优点：和 `#44` 一致
- 优点：不引入数据库驱动
- 优点：后续 `#46` 能直接复用

### 方案 B：对 `recovery_runs` 单独引入执行器，因为有 `BIGSERIAL`

- 优点：更贴近真实 insert-returning 流程
- 缺点：现在还没有 DB 执行层，会让 `#45` 过度复杂

### 方案 C：只定义 dataclass，不写 SQL

- 优点：实现快
- 缺点：不能体现 repository 行为

## 选型

采用方案 A。

## 设计

### 路径

- `src/perp_platform/store/postgres/repositories/tradeability.py`
- `src/perp_platform/store/postgres/repositories/recovery.py`
- `tests/perp_platform/store/test_postgres_tradeability_recovery.py`

### Tradeability repository

定义：

- `TradeabilityStateRecord`
- `PostgresTradeabilityRepository`

最小方法：

- `build_upsert(record) -> PostgresStatement`
- `build_select_scope(scope_type, venue_code, account_key, instrument_id) -> PostgresStatement`
- `build_select_for_account(venue_code, account_key) -> PostgresStatement`

字段：

- `scope_type`
- `venue_code`
- `account_key`
- `instrument_id`
- `supervisor_state`
- `allow_open`
- `allow_reduce`
- `reason`
- `updated_at`

upsert conflict key：

- `(scope_type, venue_code, account_key, instrument_id)`

### Recovery repository

定义：

- `RecoveryRunStartRecord`
- `RecoveryRunCompletionRecord`
- `PostgresRecoveryRepository`

最小方法：

- `build_insert_start(record) -> PostgresStatement`
- `build_mark_completed(record) -> PostgresStatement`
- `build_select_recent_runs(venue_code, account_key, limit) -> PostgresStatement`

`build_insert_start()`：

- 插入 `recovery_runs`
- 不负责真正拿 `RETURNING recovery_run_id`
- SQL 里可以包含 `RETURNING recovery_run_id`

`build_mark_completed()`：

- 通过 `recovery_run_id` 更新：
  - `status`
  - `blockers_json`
  - `completed_at`

### JSON 字段策略

`blockers_json` 在 params 里先以 JSON string 传递，不在本 issue 引入 JSON adapter。

## 测试策略

新增 `tests/perp_platform/store/test_postgres_tradeability_recovery.py`：

- tradeability upsert SQL 命中表名与 conflict key
- tradeability select SQL 按 scope 精确过滤
- recovery insert SQL 命中 `RETURNING recovery_run_id`
- recovery complete SQL 按 `recovery_run_id` 更新
- recent runs select SQL 正确排序并带 limit

## 非目标

- 不执行 SQL
- 不实现 orders / positions / balances repository 以外的 join 查询
- 不引入 DB driver
- 不写 integration test（留给 `#46`）
