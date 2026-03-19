from __future__ import annotations

import importlib
import sys
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

SRC_ROOT = Path(__file__).resolve().parents[3] / "src"
PERP_PLATFORM_ENV_KEYS = (
    "PERP_PLATFORM_APP_NAME",
    "PERP_PLATFORM_ENVIRONMENT",
    "PERP_PLATFORM_LOG_LEVEL",
)


def _clear_cached_modules() -> None:
    for name in list(sys.modules):
        if name == "perp_platform" or name.startswith("perp_platform."):
            sys.modules.pop(name, None)


@contextmanager
def local_source_path() -> Iterator[None]:
    sys.path.insert(0, str(SRC_ROOT))
    try:
        yield
    finally:
        sys.path.pop(0)


def import_perp_platform_module(module_name: str):
    _clear_cached_modules()
    with local_source_path():
        return importlib.import_module(module_name)


def load_config_module():
    return import_perp_platform_module("perp_platform.config")


def make_test_config(
    *,
    app_name: str = "perp-platform",
    environment: str = "dev",
    log_level: str = "INFO",
):
    config_module = load_config_module()
    return config_module.load_config(
        {
            "PERP_PLATFORM_APP_NAME": app_name,
            "PERP_PLATFORM_ENVIRONMENT": environment,
            "PERP_PLATFORM_LOG_LEVEL": log_level,
        }
    )
