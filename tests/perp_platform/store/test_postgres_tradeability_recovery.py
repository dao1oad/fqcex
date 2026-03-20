from tests.perp_platform.support.config import import_perp_platform_module


def _repositories_module():
    return import_perp_platform_module("perp_platform.store.postgres.repositories")


def test_tradeability_upsert_sql_contains_table_and_conflict_key() -> None:
    repositories = _repositories_module()
    repo = repositories.PostgresTradeabilityRepository()
    record = repositories.TradeabilityStateRecord(
        scope_type="instrument",
        venue_code="bybit",
        account_key="acct-001",
        instrument_id="BTCUSDT-PERP",
        supervisor_state="LIVE",
        allow_open=True,
        allow_reduce=True,
        reason="healthy",
        updated_at="2026-03-20T00:00:00Z",
    )

    statement = repo.build_upsert(record)

    assert "INSERT INTO tradeability_states" in statement.sql
    assert (
        "ON CONFLICT (scope_type, venue_code, account_key, instrument_id)"
        in statement.sql
    )
    assert statement.params["scope_type"] == "instrument"
    assert statement.params["allow_open"] is True


def test_tradeability_select_scope_filters_by_exact_scope_fields() -> None:
    repositories = _repositories_module()
    statement = repositories.PostgresTradeabilityRepository().build_select_scope(
        scope_type="instrument",
        venue_code="okx",
        account_key="acct-scope",
        instrument_id="ETHUSDT-PERP",
    )

    assert "WHERE scope_type = %(scope_type)s" in statement.sql
    assert "AND venue_code = %(venue_code)s" in statement.sql
    assert "AND account_key = %(account_key)s" in statement.sql
    assert "AND instrument_id = %(instrument_id)s" in statement.sql
    assert statement.params == {
        "scope_type": "instrument",
        "venue_code": "okx",
        "account_key": "acct-scope",
        "instrument_id": "ETHUSDT-PERP",
    }


def test_recovery_insert_includes_returning_recovery_run_id() -> None:
    repositories = _repositories_module()
    repo = repositories.PostgresRecoveryRepository()
    record = repositories.RecoveryRunStartRecord(
        venue_code="binance",
        account_key="acct-002",
        phase="RECONNECTING",
        status="RUNNING",
        trigger_reason="private_stream_down",
        blockers_json='["private_stream_down"]',
        started_at="2026-03-20T00:01:00Z",
    )

    statement = repo.build_insert_start(record)

    assert "INSERT INTO recovery_runs" in statement.sql
    assert "RETURNING recovery_run_id" in statement.sql
    assert statement.params["blockers_json"] == '["private_stream_down"]'


def test_recovery_completion_updates_by_recovery_run_id() -> None:
    repositories = _repositories_module()
    repo = repositories.PostgresRecoveryRepository()
    record = repositories.RecoveryRunCompletionRecord(
        recovery_run_id=42,
        status="COMPLETED",
        blockers_json="[]",
        completed_at="2026-03-20T00:05:00Z",
    )

    statement = repo.build_mark_completed(record)

    assert "UPDATE recovery_runs" in statement.sql
    assert "WHERE recovery_run_id = %(recovery_run_id)s" in statement.sql
    assert statement.params["recovery_run_id"] == 42


def test_recent_runs_select_sorts_and_limits_correctly() -> None:
    repositories = _repositories_module()
    statement = repositories.PostgresRecoveryRepository().build_select_recent_runs(
        venue_code="bybit",
        account_key="acct-003",
        limit=25,
    )

    assert "FROM recovery_runs" in statement.sql
    assert "ORDER BY started_at DESC, recovery_run_id DESC" in statement.sql
    assert "LIMIT %(limit)s" in statement.sql
    assert statement.params == {
        "venue_code": "bybit",
        "account_key": "acct-003",
        "limit": 25,
    }
