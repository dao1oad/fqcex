"""SQL builders for tradeability truth storage in PostgreSQL."""

from dataclasses import asdict, dataclass

from .base import PostgresStatement


@dataclass(frozen=True)
class TradeabilityStateRecord:
    scope_type: str
    venue_code: str
    account_key: str
    instrument_id: str
    supervisor_state: str
    allow_open: bool
    allow_reduce: bool
    reason: str
    updated_at: str


class PostgresTradeabilityRepository:
    """Build SQL statements for the tradeability_states table."""

    def build_upsert(self, record: TradeabilityStateRecord) -> PostgresStatement:
        return PostgresStatement(
            sql=(
                "INSERT INTO tradeability_states ("
                "scope_type, venue_code, account_key, instrument_id, "
                "supervisor_state, allow_open, allow_reduce, reason, updated_at"
                ") VALUES ("
                "%(scope_type)s, %(venue_code)s, %(account_key)s, %(instrument_id)s, "
                "%(supervisor_state)s, %(allow_open)s, %(allow_reduce)s, "
                "%(reason)s, %(updated_at)s"
                ") ON CONFLICT (scope_type, venue_code, account_key, instrument_id) "
                "DO UPDATE SET "
                "supervisor_state = EXCLUDED.supervisor_state, "
                "allow_open = EXCLUDED.allow_open, "
                "allow_reduce = EXCLUDED.allow_reduce, "
                "reason = EXCLUDED.reason, "
                "updated_at = EXCLUDED.updated_at"
            ),
            params=asdict(record),
        )

    def build_select_scope(
        self,
        scope_type: str,
        venue_code: str,
        account_key: str,
        instrument_id: str,
    ) -> PostgresStatement:
        return PostgresStatement(
            sql=(
                "SELECT scope_type, venue_code, account_key, instrument_id, "
                "supervisor_state, allow_open, allow_reduce, reason, updated_at "
                "FROM tradeability_states "
                "WHERE scope_type = %(scope_type)s "
                "AND venue_code = %(venue_code)s "
                "AND account_key = %(account_key)s "
                "AND instrument_id = %(instrument_id)s"
            ),
            params={
                "scope_type": scope_type,
                "venue_code": venue_code,
                "account_key": account_key,
                "instrument_id": instrument_id,
            },
        )

    def build_select_for_account(
        self,
        venue_code: str,
        account_key: str,
    ) -> PostgresStatement:
        return PostgresStatement(
            sql=(
                "SELECT scope_type, venue_code, account_key, instrument_id, "
                "supervisor_state, allow_open, allow_reduce, reason, updated_at "
                "FROM tradeability_states "
                "WHERE venue_code = %(venue_code)s "
                "AND account_key = %(account_key)s "
                "ORDER BY scope_type, venue_code, account_key, instrument_id"
            ),
            params={"venue_code": venue_code, "account_key": account_key},
        )
