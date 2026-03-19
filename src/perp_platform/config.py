from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

ALLOWED_ENVIRONMENTS = frozenset({"dev", "test", "prod"})
ALLOWED_LOG_LEVELS = frozenset({"DEBUG", "INFO", "WARNING", "ERROR"})


@dataclass(frozen=True)
class AppConfig:
    app_name: str
    environment: str
    log_level: str


def load_config(environ: Mapping[str, str] | None = None) -> AppConfig:
    source = {} if environ is None else environ
    app_name = source.get("PERP_PLATFORM_APP_NAME", "perp-platform").strip() or "perp-platform"
    environment = source.get("PERP_PLATFORM_ENVIRONMENT", "dev").strip().lower()
    log_level = source.get("PERP_PLATFORM_LOG_LEVEL", "INFO").strip().upper()

    if environment not in ALLOWED_ENVIRONMENTS:
        raise ValueError(
            "PERP_PLATFORM_ENVIRONMENT must be one of: dev, test, prod"
        )

    if log_level not in ALLOWED_LOG_LEVELS:
        raise ValueError(
            "PERP_PLATFORM_LOG_LEVEL must be one of: DEBUG, INFO, WARNING, ERROR"
        )

    return AppConfig(
        app_name=app_name,
        environment=environment,
        log_level=log_level,
    )
