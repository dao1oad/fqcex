from __future__ import annotations

import importlib
import sys
from pathlib import Path

import pytest

SRC_ROOT = Path(__file__).resolve().parents[2] / "src"


def test_load_config_returns_defaults() -> None:
    sys.path.insert(0, str(SRC_ROOT))
    try:
        config_module = importlib.import_module("perp_platform.config")
    finally:
        sys.path.pop(0)

    config = config_module.load_config({})

    assert config == config_module.AppConfig(
        app_name="perp-platform",
        environment="dev",
        log_level="INFO",
    )


def test_load_config_rejects_invalid_environment() -> None:
    sys.path.insert(0, str(SRC_ROOT))
    try:
        config_module = importlib.import_module("perp_platform.config")
    finally:
        sys.path.pop(0)

    with pytest.raises(ValueError, match="PERP_PLATFORM_ENVIRONMENT"):
        config_module.load_config({"PERP_PLATFORM_ENVIRONMENT": "staging"})


def test_load_config_rejects_invalid_log_level() -> None:
    sys.path.insert(0, str(SRC_ROOT))
    try:
        config_module = importlib.import_module("perp_platform.config")
    finally:
        sys.path.pop(0)

    with pytest.raises(ValueError, match="PERP_PLATFORM_LOG_LEVEL"):
        config_module.load_config({"PERP_PLATFORM_LOG_LEVEL": "TRACE"})
