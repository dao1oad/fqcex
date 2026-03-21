# Issue 69 Read Models Design

## Goal

为 Phase 4 控制平面定义最小的可交易性与恢复读模型，使外部消费者知道哪些字段来自现有 `Supervisor` 投影和 truth store，而不提前实现查询 API。

## Scope

- 修改 `docs/architecture/control-plane-api.md`
- 修改 `docs/architecture/DATA_MODEL.md`
- 新增一个 governance contract test

## Recommendation

把 `#69` 收口为三种读模型：

- Venue Tradeability Read Model
- Instrument Tradeability Read Model
- Recovery Run Read Model

它们都必须显式绑定到现有 `tradeability_states` / `recovery_runs` 真相表或 `Supervisor` 投影，而不是引入新的 truth source。
