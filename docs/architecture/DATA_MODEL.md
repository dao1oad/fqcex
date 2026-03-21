# DATA_MODEL

## Canonical Instrument

- `instrument_id = BASE-QUOTE-PERP`
- Example: `BTC-USDT-PERP`

## Core Truth Fields

- Canonical quantity truth: `base_qty`
- Risk notional: `notional_usdt`
- Risk valuation price: `mark_price`
- Venue payload fields remain edge-only:
  - `exchange_qty`
  - `exchange_qty_kind`

## Quantity Rules

- Truth quantity: `base_qty`
- Risk notional: `notional_usdt`
- Edge fields:
  - `exchange_qty`
  - `exchange_qty_kind`

## Venue Quantity Mapping

- Bybit: `base_qty = qty`
- Binance: `base_qty = quantity`
- OKX: `base_qty = sz * base_per_exchange_qty`

## Boundary Constraints

- `exchange-specific` quantity fields stay at the adapter boundary
- Core model truth stays venue-neutral and only projects canonical fields such as `base_qty`
- Venue conversion rules exist to normalize edge payloads into canonical truth, not to leak exchange-specific shape into the core model

## Position Scope

- `one_way`
- `isolated`
- `mark_price` based risk valuation

## Minimum Truth Store Tables

- `venues`
- `accounts`
- `instruments`
- `connection_states`
- `tradeability_states`
- `recovery_runs`
- `orders`
- `positions`
- `balances`

## Truth Store Initialization

- PostgreSQL truth store 以 `migrations/postgres/0001_core_truth_schema.sql` 作为最小初始化入口
- `CORE_TRUTH_TABLES` 是当前 Phase 2 的最小表集真相
- schema 与 repository contract 必须围绕同一组表名工作，不能在边界外引入额外真相表

## Persistence Mapping

- `orders`
  - 保存订单真相与边界字段：`base_qty`、`exchange_qty`、`exchange_qty_kind`
- `positions`
  - 保存仓位与风险字段：`base_qty`、`mark_price`、`notional_usdt`
- `balances`
  - 保存账户余额真相：`wallet_balance`、`available_balance`
- `tradeability_states`
  - 保存 Supervisor 投影真相：`supervisor_state`、`allow_open`、`allow_reduce`
- `recovery_runs`
  - 保存恢复过程元数据：`phase`、`status`、`trigger_reason`、`blockers_json`

## Control Plane Read Models

控制平面读模型只消费现有真相表与 `Supervisor` 投影，不新增新的 truth source。

### Venue Tradeability Read Model

- 读取来源：`tradeability_states`
- 投影字段：`venue`、`supervisor_state`、`allow_open`、`allow_reduce`
- 语义：对外暴露 venue 级 tradeability projection

### Instrument Tradeability Read Model

- 读取来源：`tradeability_states`
- 投影字段：`instrument_id`、`venue`、`supervisor_state`、`allow_open`、`allow_reduce`
- 语义：对外暴露 instrument 级 tradeability projection

### Recovery Run Read Model

- 读取来源：`recovery_runs`
- 投影字段：`run_id`、`phase`、`status`、`trigger_reason`、`blockers_json`
- 语义：对外暴露恢复过程状态与阻断原因

## Audit Storage Boundary

- `audit_events`
  - 归属：append-only PostgreSQL 审计层
  - 作用：保存 operator action、recovery 和 supervisor state change 的结构化留痕
  - 约束：not part of the core trading truth tables
- incident narrative、dry-run evidence 和外部 closeout 文档不进入 `audit_events`
