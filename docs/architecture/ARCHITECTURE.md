# ARCHITECTURE

## Objective

Build a connection management platform for multi-exchange perpetual futures arbitrage.

## Core Components

- `NautilusTrader runtime`
  - Primary venue connectivity
  - Execution
  - Reconciliation
  - Portfolio and risk primitives
- `Supervisor`
  - Tradeability truth source
  - Recovery orchestration
  - Manual operator controls
- `Cryptofeed checker`
  - Independent market data validation
  - Freshness and divergence signals
- `PostgreSQL`
  - Current truth state
  - Recovery metadata
- `Audit logs`
  - Recovery trail
  - Operator action trail
- `Control Plane`
  - Read-mostly projection surface for external operators and dashboards
  - Projects `Supervisor`, store, checker, and audit views without taking truth ownership

## Phase 1 Topology

- `nautilus-runtime-bybit`
- `nautilus-runtime-binance`
- `nautilus-runtime-okx`
- `supervisor`
- `cryptofeed-checker`

## Truth Ownership

- Orders, positions, balances: Nautilus runtime path
- Tradeability: Supervisor
- Independent market suspicion signals: Cryptofeed checker
- Control plane responses: projections from Supervisor/store/audit without changing truth ownership

## Platformization Boundary

- `NautilusTrader runtime` 继续负责 venue 连接、执行和订单/仓位/余额真相
- `Supervisor` remains the tradeability truth source
- `Control Plane remains projection-only`
- `Control Plane` 只读取 `Supervisor`、store、checker 和 audit 的投影视图
- `Audit logs` 负责保留恢复与操作员留痕，但不声明系统真相
- Phase 4 的平台化不改变 Phase 1-3 已冻结的 truth ownership

## Migration Plan

1. 先冻结 control-plane api surface、operator action boundary 和 read models
2. 再冻结 audit 事件、存储边界与运行手册
3. 保持 runtime、Supervisor、store 的主真相链路不变
4. 仅在文档边界稳定后，才考虑后续 transport、service split 或控制平面实现

## Checker Boundary

- `Cryptofeed checker` uses venue `TICKER` streams as the independent Phase 1 top-of-book source for `Bybit`, `Binance Futures`, and `OKX`.
- Checker normalization stays at the boundary layer:
  - canonical instrument ids remain `*-USDT-PERP`
  - venue-native exchange symbols remain attached for diagnostics
  - venue-specific top-of-book size fields are extracted from raw payloads and normalized into unified `bid_size` / `ask_size`
- Checker policy evaluation stays separate from Supervisor truth:
  - freshness uses `receipt_timestamp` and local age calculation
  - divergence compares same-venue same-instrument bid/ask in basis points against a reference top-of-book
  - policy output is an intermediate judgment, not a direct Supervisor state override
- Checker signal mapping is a separate projection step:
  - healthy policies project to `SupervisorState.LIVE`
  - stale checker data projects to `SupervisorState.DEGRADED`
  - top-of-book divergence projects to `SupervisorState.RESYNCING`
  - Supervisor remains the tradeability truth source even when checker suggests a stricter state
- Symbol mapping is primed with the frozen Phase 1 instrument set so checker startup does not depend on live symbol discovery.
