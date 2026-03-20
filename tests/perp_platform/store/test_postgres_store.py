from pathlib import Path

from tests.perp_platform.support.config import import_perp_platform_module


def _store_module():
    return import_perp_platform_module("perp_platform.store")


def _postgres_module():
    return import_perp_platform_module("perp_platform.store.postgres")


def _repositories_module():
    return import_perp_platform_module("perp_platform.store.postgres.repositories")


def test_store_package_exposes_postgres_contract_entrypoints() -> None:
    store = _store_module()
    postgres = _postgres_module()

    assert store.PostgresStoreSchemaVersion == postgres.CORE_SCHEMA_VERSION
    assert store.PostgresStoreTables == postgres.CORE_TRUTH_TABLES
    assert store.PostgresRepositories.__name__ == postgres.repositories.__name__


def test_store_contract_covers_required_truth_tables_and_builders() -> None:
    postgres = _postgres_module()
    repositories = _repositories_module()

    required_tables = {
        "orders",
        "positions",
        "balances",
        "tradeability_states",
        "recovery_runs",
    }
    assert required_tables.issubset(set(postgres.CORE_TRUTH_TABLES))
    assert repositories.PostgresOrdersRepository
    assert repositories.PostgresPositionsRepository
    assert repositories.PostgresBalancesRepository
    assert repositories.PostgresTradeabilityRepository
    assert repositories.PostgresRecoveryRepository


def test_store_contract_preserves_canonical_truth_fields_across_schema_and_sql() -> None:
    postgres = _postgres_module()
    repositories = _repositories_module()

    schema_sql = postgres.CORE_SCHEMA_SQL
    position_sql = repositories.PostgresPositionsRepository().build_upsert(
        repositories.PositionRecord(
            venue_code="okx",
            account_key="acct-001",
            instrument_id="BTC-USDT-PERP",
            base_qty="1.000000000000000000",
            mark_price="65000.000000000000000000",
            notional_usdt="65000.000000000000000000",
            position_mode="one_way",
            margin_mode="isolated",
            leverage="2.000000000000000000",
            updated_at="2026-03-20T00:00:00Z",
        )
    ).sql
    tradeability_sql = repositories.PostgresTradeabilityRepository().build_upsert(
        repositories.TradeabilityStateRecord(
            scope_type="instrument",
            venue_code="bybit",
            account_key="acct-001",
            instrument_id="BTC-USDT-PERP",
            supervisor_state="LIVE",
            allow_open=True,
            allow_reduce=True,
            reason="healthy",
            updated_at="2026-03-20T00:00:00Z",
        )
    ).sql
    recovery_sql = repositories.PostgresRecoveryRepository().build_insert_start(
        repositories.RecoveryRunStartRecord(
            venue_code="binance",
            account_key="acct-001",
            phase="RECONNECTING",
            status="RUNNING",
            trigger_reason="private_stream_down",
            blockers_json='["private_stream_down"]',
            started_at="2026-03-20T00:00:00Z",
        )
    ).sql

    assert "base_qty" in schema_sql
    assert "mark_price" in schema_sql
    assert "notional_usdt" in schema_sql
    assert "supervisor_state" in schema_sql
    assert "blockers_json" in schema_sql
    assert "base_qty" in position_sql
    assert "mark_price" in position_sql
    assert "notional_usdt" in position_sql
    assert "supervisor_state" in tradeability_sql
    assert "blockers_json" in recovery_sql


def test_data_model_documents_truth_store_initialization_and_persistence_mapping() -> None:
    document = Path("docs/architecture/DATA_MODEL.md").read_text(encoding="utf-8")

    assert "## Truth Store Initialization" in document
    assert "migrations/postgres/0001_core_truth_schema.sql" in document
    assert "## Persistence Mapping" in document
    assert "`tradeability_states`" in document
    assert "`recovery_runs`" in document
    assert "`blockers_json`" in document
