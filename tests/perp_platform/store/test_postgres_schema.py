from pathlib import Path

from tests.perp_platform.support.config import import_perp_platform_module


def _schema_module():
    return import_perp_platform_module("perp_platform.store.postgres.schema")


def test_schema_module_import_and_version() -> None:
    schema = _schema_module()

    assert schema.CORE_SCHEMA_VERSION == "0001"
    assert schema.CORE_SCHEMA_SQL


def test_core_truth_tables_contains_all_required_tables() -> None:
    schema = _schema_module()

    expected = {
        "venues",
        "accounts",
        "instruments",
        "connection_states",
        "tradeability_states",
        "recovery_runs",
        "orders",
        "positions",
        "balances",
    }
    assert set(schema.CORE_TRUTH_TABLES) == expected


def test_migration_file_exists() -> None:
    migration_path = Path("migrations/postgres/0001_core_truth_schema.sql")
    assert migration_path.exists()


def test_migration_contains_required_tables_and_fields() -> None:
    migration_sql = Path("migrations/postgres/0001_core_truth_schema.sql").read_text(
        encoding="utf-8"
    )

    required_tables = {
        "venues",
        "accounts",
        "instruments",
        "connection_states",
        "tradeability_states",
        "recovery_runs",
        "orders",
        "positions",
        "balances",
    }
    for table_name in required_tables:
        assert f"CREATE TABLE IF NOT EXISTS {table_name}" in migration_sql

    for field_name in (
        "base_qty",
        "mark_price",
        "notional_usdt",
        "supervisor_state",
        "blockers_json",
    ):
        assert field_name in migration_sql
