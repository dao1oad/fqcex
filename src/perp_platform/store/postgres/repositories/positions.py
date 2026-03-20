"""SQL builders for positions truth storage in PostgreSQL."""

from dataclasses import asdict, dataclass

from .base import PostgresStatement


@dataclass(frozen=True)
class PositionRecord:
    venue_code: str
    account_key: str
    instrument_id: str
    base_qty: str
    mark_price: str
    notional_usdt: str
    position_mode: str
    margin_mode: str
    leverage: str
    updated_at: str


class PostgresPositionsRepository:
    """Build SQL statements for the positions table."""

    def build_upsert(self, record: PositionRecord) -> PostgresStatement:
        return PostgresStatement(
            sql=(
                "INSERT INTO positions ("
                "venue_code, account_key, instrument_id, base_qty, mark_price, "
                "notional_usdt, position_mode, margin_mode, leverage, updated_at"
                ") VALUES ("
                "%(venue_code)s, %(account_key)s, %(instrument_id)s, %(base_qty)s, "
                "%(mark_price)s, %(notional_usdt)s, %(position_mode)s, "
                "%(margin_mode)s, %(leverage)s, %(updated_at)s"
                ") ON CONFLICT (venue_code, account_key, instrument_id) DO UPDATE SET "
                "base_qty = EXCLUDED.base_qty, "
                "mark_price = EXCLUDED.mark_price, "
                "notional_usdt = EXCLUDED.notional_usdt, "
                "position_mode = EXCLUDED.position_mode, "
                "margin_mode = EXCLUDED.margin_mode, "
                "leverage = EXCLUDED.leverage, "
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
                "SELECT venue_code, account_key, instrument_id, base_qty, mark_price, "
                "notional_usdt, position_mode, margin_mode, leverage, updated_at "
                "FROM positions "
                "WHERE venue_code = %(venue_code)s "
                "AND account_key = %(account_key)s "
                "ORDER BY venue_code, account_key, instrument_id"
            ),
            params={"venue_code": venue_code, "account_key": account_key},
        )
