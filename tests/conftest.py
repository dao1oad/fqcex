from __future__ import annotations

import pytest

PERP_PLATFORM_ENV_KEYS = (
    "PERP_PLATFORM_APP_NAME",
    "PERP_PLATFORM_ENVIRONMENT",
    "PERP_PLATFORM_LOG_LEVEL",
)


@pytest.fixture(autouse=True)
def clear_perp_platform_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    for key in PERP_PLATFORM_ENV_KEYS:
        monkeypatch.delenv(key, raising=False)
