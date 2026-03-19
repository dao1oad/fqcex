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
