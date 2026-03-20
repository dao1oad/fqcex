"""SQL builders for balances truth storage in PostgreSQL."""

from dataclasses import asdict, dataclass

from .base import PostgresStatement


@dataclass(frozen=True)
class BalanceRecord:
    venue_code: str
    account_key: str
    asset: str
    wallet_balance: str
    available_balance: str
    updated_at: str


class PostgresBalancesRepository:
    """Build SQL statements for the balances table."""

    def build_upsert(self, record: BalanceRecord) -> PostgresStatement:
        return PostgresStatement(
            sql=(
                "INSERT INTO balances ("
                "venue_code, account_key, asset, wallet_balance, available_balance, "
                "updated_at"
                ") VALUES ("
                "%(venue_code)s, %(account_key)s, %(asset)s, %(wallet_balance)s, "
                "%(available_balance)s, %(updated_at)s"
                ") ON CONFLICT (venue_code, account_key, asset) DO UPDATE SET "
                "wallet_balance = EXCLUDED.wallet_balance, "
                "available_balance = EXCLUDED.available_balance, "
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
                "SELECT venue_code, account_key, asset, wallet_balance, "
                "available_balance, updated_at "
                "FROM balances "
                "WHERE venue_code = %(venue_code)s "
                "AND account_key = %(account_key)s "
                "ORDER BY venue_code, account_key, asset"
            ),
            params={"venue_code": venue_code, "account_key": account_key},
        )
