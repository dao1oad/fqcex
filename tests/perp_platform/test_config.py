from __future__ import annotations

import pytest
from tests.perp_platform.support import load_config_module


def test_load_config_returns_defaults() -> None:
    config_module = load_config_module()

    config = config_module.load_config({})

    assert config == config_module.AppConfig(
        app_name="perp-platform",
        environment="dev",
        log_level="INFO",
    )


def test_load_config_rejects_invalid_environment() -> None:
    config_module = load_config_module()

    with pytest.raises(ValueError, match="PERP_PLATFORM_ENVIRONMENT"):
        config_module.load_config({"PERP_PLATFORM_ENVIRONMENT": "staging"})


def test_load_config_rejects_invalid_log_level() -> None:
    config_module = load_config_module()

    with pytest.raises(ValueError, match="PERP_PLATFORM_LOG_LEVEL"):
        config_module.load_config({"PERP_PLATFORM_LOG_LEVEL": "TRACE"})
