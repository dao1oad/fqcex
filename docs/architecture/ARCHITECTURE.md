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
