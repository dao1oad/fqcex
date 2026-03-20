"""SQL builders for orders truth storage in PostgreSQL."""

from dataclasses import asdict, dataclass

from .base import PostgresStatement


@dataclass(frozen=True)
class OrderRecord:
    venue_code: str
    account_key: str
    order_id: str
    instrument_id: str
    status: str
    order_type: str
    time_in_force: str
    reduce_only: bool
    side: str
    base_qty: str
    exchange_qty: str
    exchange_qty_kind: str
    price: str | None
    updated_at: str


class PostgresOrdersRepository:
    """Build SQL statements for the orders table."""

    def build_upsert(self, record: OrderRecord) -> PostgresStatement:
        return PostgresStatement(
            sql=(
                "INSERT INTO orders ("
                "venue_code, account_key, order_id, instrument_id, status, "
                "order_type, time_in_force, reduce_only, side, base_qty, "
                "exchange_qty, exchange_qty_kind, price, updated_at"
                ") VALUES ("
                "%(venue_code)s, %(account_key)s, %(order_id)s, %(instrument_id)s, "
                "%(status)s, %(order_type)s, %(time_in_force)s, %(reduce_only)s, "
                "%(side)s, %(base_qty)s, %(exchange_qty)s, %(exchange_qty_kind)s, "
                "%(price)s, %(updated_at)s"
                ") ON CONFLICT (venue_code, account_key, order_id) DO UPDATE SET "
                "instrument_id = EXCLUDED.instrument_id, "
                "status = EXCLUDED.status, "
                "order_type = EXCLUDED.order_type, "
                "time_in_force = EXCLUDED.time_in_force, "
                "reduce_only = EXCLUDED.reduce_only, "
                "side = EXCLUDED.side, "
                "base_qty = EXCLUDED.base_qty, "
                "exchange_qty = EXCLUDED.exchange_qty, "
                "exchange_qty_kind = EXCLUDED.exchange_qty_kind, "
                "price = EXCLUDED.price, "
                "updated_at = EXCLUDED.updated_at"
            ),
            params=asdict(record),
        )

    def build_select_for_account(
        self,
        venue_code: str,
        account_key: str,
    ) -> PostgresStatement:
        return PostgresStatement(
            sql=(
                "SELECT venue_code, account_key, order_id, instrument_id, status, "
                "order_type, time_in_force, reduce_only, side, base_qty, "
                "exchange_qty, exchange_qty_kind, price, updated_at "
                "FROM orders "
                "WHERE venue_code = %(venue_code)s "
                "AND account_key = %(account_key)s "
                "ORDER BY venue_code, account_key, order_id"
            ),
            params={"venue_code": venue_code, "account_key": account_key},
        )
