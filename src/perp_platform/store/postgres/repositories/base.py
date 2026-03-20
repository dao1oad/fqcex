"""Base SQL statement contract for PostgreSQL truth repositories."""

from dataclasses import dataclass


@dataclass(frozen=True)
class PostgresStatement:
    """A SQL statement with named parameters."""

    sql: str
    params: dict[str, object]
