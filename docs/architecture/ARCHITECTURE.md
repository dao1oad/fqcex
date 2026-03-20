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
