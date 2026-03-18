# DATA_MODEL

## Canonical Instrument

- `instrument_id = BASE-QUOTE-PERP`
- Example: `BTC-USDT-PERP`

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

## Position Scope

- `one_way`
- `isolated`
- mark-price based risk valuation

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
