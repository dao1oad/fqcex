"""Core PostgreSQL schema contract for truth storage."""

from pathlib import Path

TABLE_VENUES = "venues"
TABLE_ACCOUNTS = "accounts"
TABLE_INSTRUMENTS = "instruments"
TABLE_CONNECTION_STATES = "connection_states"
TABLE_TRADEABILITY_STATES = "tradeability_states"
TABLE_RECOVERY_RUNS = "recovery_runs"
TABLE_ORDERS = "orders"
TABLE_POSITIONS = "positions"
TABLE_BALANCES = "balances"

CORE_TRUTH_TABLES = (
    TABLE_VENUES,
    TABLE_ACCOUNTS,
    TABLE_INSTRUMENTS,
    TABLE_CONNECTION_STATES,
    TABLE_TRADEABILITY_STATES,
    TABLE_RECOVERY_RUNS,
    TABLE_ORDERS,
    TABLE_POSITIONS,
    TABLE_BALANCES,
)

CORE_SCHEMA_VERSION = "0001"
_MIGRATION_PATH = (
    Path(__file__).resolve().parents[4]
    / "migrations"
    / "postgres"
    / f"{CORE_SCHEMA_VERSION}_core_truth_schema.sql"
)
CORE_SCHEMA_SQL = _MIGRATION_PATH.read_text(encoding="utf-8")
