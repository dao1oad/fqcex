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
4. 在文档边界稳定后，先进入 live readiness 阶段，落地最小 control-plane backend、operator gate、audit query 和 live canary 闭环
5. 仅在 live readiness closeout 完成后，才考虑 native adapter 替换、service split 或更激进的平台拆分

## Live Readiness Boundary

- `NautilusTrader runtime` 继续负责真实 venue 连接、执行、reconciliation 和订单 / 仓位 / 余额真相
- `Supervisor` 继续负责 tradeability truth 与 `LIVE / DEGRADED / RESYNCING / REDUCE_ONLY / BLOCKED` 投影
- `Control Plane` 在 live readiness 阶段实现为 read-mostly service：
  - 暴露 venue / instrument / recovery / checker / audit 投影视图
  - 提供受控 operator actions
- `Audit logs` 继续是 append-only trail，不替代 runtime/store/Supervisor 真相
- live canary 的 closeout 只代表小资金、受控 allowlist 范围内的真实环境验收，不自动升级为大规模放量许可

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
