# ADR 0002: Phase 1 Covers USDT Linear Perpetuals Only

## Context

Expanding phase 1 to spot, options, or coin-margined derivatives would multiply symbol, position, and risk model complexity.

## Decision

Restrict phase 1 to `USDT` linear perpetual contracts only.

## Consequences

- Cleaner instrument and quantity model
- Lower recovery and reconciliation complexity
- Faster validation of cross-exchange arbitrage infrastructure
- Product expansion moves to later phases
