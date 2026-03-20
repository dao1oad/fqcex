from tests.perp_platform.support.config import import_perp_platform_module


def _repositories_module():
    return import_perp_platform_module("perp_platform.store.postgres.repositories")


def test_orders_upsert_sql_includes_table_and_conflict_key() -> None:
    repositories = _repositories_module()
    repo = repositories.PostgresOrdersRepository()
    record = repositories.OrderRecord(
        venue_code="bybit",
        account_key="acct-001",
        order_id="order-123",
        instrument_id="BTCUSDT-PERP",
        status="NEW",
        order_type="LIMIT",
        time_in_force="GTC",
        reduce_only=False,
        side="BUY",
        base_qty="0.010000000000000000",
        exchange_qty="0.010000000000000000",
        exchange_qty_kind="base",
        price="65000.000000000000000000",
        updated_at="2026-03-20T00:00:00Z",
    )

    statement = repo.build_upsert(record)

    assert "INSERT INTO orders" in statement.sql
    assert "ON CONFLICT (venue_code, account_key, order_id)" in statement.sql
    assert statement.params["order_id"] == "order-123"
    assert statement.params["base_qty"] == "0.010000000000000000"


def test_positions_upsert_sql_includes_canonical_quantity_and_risk_fields() -> None:
    repositories = _repositories_module()
    repo = repositories.PostgresPositionsRepository()
    record = repositories.PositionRecord(
        venue_code="okx",
        account_key="acct-002",
        instrument_id="ETHUSDT-PERP",
        base_qty="1.250000000000000000",
        mark_price="3500.000000000000000000",
        notional_usdt="4375.000000000000000000",
        position_mode="one_way",
        margin_mode="isolated",
        leverage="2.000000000000000000",
        updated_at="2026-03-20T00:05:00Z",
    )

    statement = repo.build_upsert(record)

    assert "INSERT INTO positions" in statement.sql
    for required_field in ("base_qty", "mark_price", "notional_usdt"):
        assert required_field in statement.sql
    assert statement.params["notional_usdt"] == "4375.000000000000000000"


def test_balances_upsert_sql_includes_balance_fields() -> None:
    repositories = _repositories_module()
    repo = repositories.PostgresBalancesRepository()
    record = repositories.BalanceRecord(
        venue_code="binance",
        account_key="acct-003",
        asset="USDT",
        wallet_balance="1000.000000000000000000",
        available_balance="850.000000000000000000",
        updated_at="2026-03-20T00:10:00Z",
    )

    statement = repo.build_upsert(record)

    assert "INSERT INTO balances" in statement.sql
    assert "wallet_balance" in statement.sql
    assert "available_balance" in statement.sql
    assert statement.params["asset"] == "USDT"
    assert statement.params["available_balance"] == "850.000000000000000000"


def test_select_sql_filters_and_sorts_correctly() -> None:
    repositories = _repositories_module()

    orders_statement = repositories.PostgresOrdersRepository().build_select_for_account(
        venue_code="bybit",
        account_key="acct-select",
    )
    positions_statement = (
        repositories.PostgresPositionsRepository().build_select_for_account(
            venue_code="bybit",
            account_key="acct-select",
        )
    )
    balances_statement = (
        repositories.PostgresBalancesRepository().build_select_for_account(
            venue_code="bybit",
            account_key="acct-select",
        )
    )

    assert "WHERE venue_code = %(venue_code)s" in orders_statement.sql
    assert "AND account_key = %(account_key)s" in orders_statement.sql
    assert "ORDER BY venue_code, account_key, order_id" in orders_statement.sql

    assert "ORDER BY venue_code, account_key, instrument_id" in positions_statement.sql
    assert "ORDER BY venue_code, account_key, asset" in balances_statement.sql


def test_select_params_preserve_input_values() -> None:
    repositories = _repositories_module()

    venue_code = "okx"
    account_key = "acct-params"

    orders_statement = repositories.PostgresOrdersRepository().build_select_for_account(
        venue_code=venue_code,
        account_key=account_key,
    )
    positions_statement = (
        repositories.PostgresPositionsRepository().build_select_for_account(
            venue_code=venue_code,
            account_key=account_key,
        )
    )
    balances_statement = (
        repositories.PostgresBalancesRepository().build_select_for_account(
            venue_code=venue_code,
            account_key=account_key,
        )
    )

    for statement in (orders_statement, positions_statement, balances_statement):
        assert statement.params == {
            "venue_code": venue_code,
            "account_key": account_key,
        }
