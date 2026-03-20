CREATE TABLE IF NOT EXISTS venues (
    venue_code TEXT PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS accounts (
    account_key TEXT PRIMARY KEY,
    venue_code TEXT NOT NULL REFERENCES venues(venue_code),
    account_label TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS instruments (
    instrument_id TEXT PRIMARY KEY,
    base_asset TEXT NOT NULL,
    quote_asset TEXT NOT NULL,
    kind TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS connection_states (
    venue_code TEXT NOT NULL REFERENCES venues(venue_code),
    account_key TEXT NOT NULL REFERENCES accounts(account_key),
    stream_type TEXT NOT NULL,
    status TEXT NOT NULL,
    detail_reason TEXT NOT NULL,
    observed_at TIMESTAMPTZ NOT NULL,
    PRIMARY KEY (venue_code, account_key, stream_type)
);

CREATE TABLE IF NOT EXISTS tradeability_states (
    scope_type TEXT NOT NULL,
    venue_code TEXT NOT NULL REFERENCES venues(venue_code),
    account_key TEXT NOT NULL REFERENCES accounts(account_key),
    instrument_id TEXT NOT NULL,
    supervisor_state TEXT NOT NULL,
    allow_open BOOLEAN NOT NULL,
    allow_reduce BOOLEAN NOT NULL,
    reason TEXT NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL,
    PRIMARY KEY (scope_type, venue_code, account_key, instrument_id)
);

CREATE TABLE IF NOT EXISTS recovery_runs (
    recovery_run_id BIGSERIAL PRIMARY KEY,
    venue_code TEXT NOT NULL REFERENCES venues(venue_code),
    account_key TEXT NOT NULL REFERENCES accounts(account_key),
    phase TEXT NOT NULL,
    status TEXT NOT NULL,
    trigger_reason TEXT NOT NULL,
    blockers_json JSONB NOT NULL,
    started_at TIMESTAMPTZ NOT NULL,
    completed_at TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS orders (
    venue_code TEXT NOT NULL REFERENCES venues(venue_code),
    account_key TEXT NOT NULL REFERENCES accounts(account_key),
    order_id TEXT NOT NULL,
    instrument_id TEXT NOT NULL REFERENCES instruments(instrument_id),
    status TEXT NOT NULL,
    order_type TEXT NOT NULL,
    time_in_force TEXT NOT NULL,
    reduce_only BOOLEAN NOT NULL,
    side TEXT NOT NULL,
    base_qty NUMERIC(36, 18) NOT NULL,
    exchange_qty NUMERIC(36, 18) NOT NULL,
    exchange_qty_kind TEXT NOT NULL,
    price NUMERIC(36, 18),
    updated_at TIMESTAMPTZ NOT NULL,
    PRIMARY KEY (venue_code, account_key, order_id)
);

CREATE TABLE IF NOT EXISTS positions (
    venue_code TEXT NOT NULL REFERENCES venues(venue_code),
    account_key TEXT NOT NULL REFERENCES accounts(account_key),
    instrument_id TEXT NOT NULL REFERENCES instruments(instrument_id),
    base_qty NUMERIC(36, 18) NOT NULL,
    mark_price NUMERIC(36, 18) NOT NULL,
    notional_usdt NUMERIC(36, 18) NOT NULL,
    position_mode TEXT NOT NULL,
    margin_mode TEXT NOT NULL,
    leverage NUMERIC(36, 18) NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL,
    PRIMARY KEY (venue_code, account_key, instrument_id)
);

CREATE TABLE IF NOT EXISTS balances (
    venue_code TEXT NOT NULL REFERENCES venues(venue_code),
    account_key TEXT NOT NULL REFERENCES accounts(account_key),
    asset TEXT NOT NULL,
    wallet_balance NUMERIC(36, 18) NOT NULL,
    available_balance NUMERIC(36, 18) NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL,
    PRIMARY KEY (venue_code, account_key, asset)
);
