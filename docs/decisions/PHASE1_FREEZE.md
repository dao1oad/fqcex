# PHASE1_FREEZE

## Frozen Decisions

- Exchanges: `Bybit`, `Binance`, `OKX`
- Product scope: `USDT` linear perpetuals only
- Product scope (plain): USDT linear perpetuals only
- Main runtime: `NautilusTrader`
- Checker role: `Cryptofeed` for validation only
- `Hummingbot` remains reference-only
- `position_mode = one_way`
- `margin_mode = isolated`
- default leverage `2x`, hard cap `3x`
- supported orders:
  - `LIMIT`
  - `MARKET`
  - `CANCEL`
  - `GTC`
  - `IOC`
  - `reduce_only`
- truth store: `PostgreSQL`
- default branch: `main`

## Frozen Model Constraints

- Canonical instrument for Phase 1 remains `BASE-USDT-PERP`
- Canonical truth quantity remains `base_qty`
- Venue quantity mapping stays at the adapter edge boundary
- Risk checks and unrealized PnL use `mark_price`
- Exchange-specific payload fields do not enter the core model truth unchanged

## Explicitly Deferred

- spot
- coin-margined contracts
- options
- hedge mode
- cross margin
- complex algo orders
- Hummingbot in production runtime
- heavy platformization
- native adapter replacement
