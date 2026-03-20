"""SQL builders for recovery run persistence in PostgreSQL."""

from dataclasses import asdict, dataclass

from .base import PostgresStatement


@dataclass(frozen=True)
class RecoveryRunStartRecord:
    venue_code: str
    account_key: str
    phase: str
    status: str
    trigger_reason: str
    blockers_json: str
    started_at: str


@dataclass(frozen=True)
class RecoveryRunCompletionRecord:
    recovery_run_id: int
    status: str
    blockers_json: str
    completed_at: str


class PostgresRecoveryRepository:
    """Build SQL statements for the recovery_runs table."""

    def build_insert_start(self, record: RecoveryRunStartRecord) -> PostgresStatement:
        return PostgresStatement(
            sql=(
                "INSERT INTO recovery_runs ("
                "venue_code, account_key, phase, status, trigger_reason, "
                "blockers_json, started_at"
                ") VALUES ("
                "%(venue_code)s, %(account_key)s, %(phase)s, %(status)s, "
                "%(trigger_reason)s, %(blockers_json)s, %(started_at)s"
                ") RETURNING recovery_run_id"
            ),
            params=asdict(record),
        )

    def build_mark_completed(
        self,
        record: RecoveryRunCompletionRecord,
    ) -> PostgresStatement:
        return PostgresStatement(
            sql=(
                "UPDATE recovery_runs "
                "SET status = %(status)s, "
                "blockers_json = %(blockers_json)s, "
                "completed_at = %(completed_at)s "
                "WHERE recovery_run_id = %(recovery_run_id)s"
            ),
            params=asdict(record),
        )

    def build_select_recent_runs(
        self,
        venue_code: str,
        account_key: str,
        limit: int,
    ) -> PostgresStatement:
        return PostgresStatement(
            sql=(
                "SELECT recovery_run_id, venue_code, account_key, phase, status, "
                "trigger_reason, blockers_json, started_at, completed_at "
                "FROM recovery_runs "
                "WHERE venue_code = %(venue_code)s "
                "AND account_key = %(account_key)s "
                "ORDER BY started_at DESC, recovery_run_id DESC "
                "LIMIT %(limit)s"
            ),
            params={
                "venue_code": venue_code,
                "account_key": account_key,
                "limit": limit,
            },
        )
