from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from ..config import AppConfig, load_config
from ..domain import Venue
from .config import CheckerConfig, load_checker_config


@dataclass(frozen=True)
class CheckerSubscriptionTarget:
    venue: Venue
    instrument_id: str


@dataclass(frozen=True)
class CheckerBootstrapResult:
    app_config: AppConfig
    checker_config: CheckerConfig
    service_label: str
    subscription_plan: tuple[CheckerSubscriptionTarget, ...]


def bootstrap_checker(
    environ: Mapping[str, str] | None = None,
) -> CheckerBootstrapResult:
    app_config = load_config(environ)
    checker_config = load_checker_config(environ)

    subscription_plan = tuple(
        CheckerSubscriptionTarget(venue=venue, instrument_id=instrument_id)
        for venue in checker_config.venues
        for instrument_id in checker_config.instrument_ids
    )

    return CheckerBootstrapResult(
        app_config=app_config,
        checker_config=checker_config,
        service_label=f"{checker_config.service_name}-{app_config.environment}",
        subscription_plan=subscription_plan,
    )
