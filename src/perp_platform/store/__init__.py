"""Store package for truth persistence interfaces and adapters."""

from .postgres import CORE_SCHEMA_VERSION, CORE_TRUTH_TABLES, repositories

PostgresStoreSchemaVersion = CORE_SCHEMA_VERSION
PostgresStoreTables = CORE_TRUTH_TABLES
PostgresRepositories = repositories

__all__ = [
    "PostgresRepositories",
    "PostgresStoreSchemaVersion",
    "PostgresStoreTables",
]
