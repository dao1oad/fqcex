from __future__ import annotations

import os

import pytest

from tests.perp_platform.support import make_test_config, run_cli


def test_make_test_config_returns_app_config() -> None:
    config = make_test_config(environment="test")

    assert config.environment == "test"
    assert config.log_level == "INFO"


def test_run_cli_returns_exit_code_and_stdout() -> None:
    result = run_cli(env={"PERP_PLATFORM_ENVIRONMENT": "test"})

    assert result.exit_code == 0
    assert result.stdout == "perp-platform bootstrap ready [test]"


def test_run_cli_restores_environment_after_call(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("PERP_PLATFORM_ENVIRONMENT", "prod")

    run_cli(env={"PERP_PLATFORM_ENVIRONMENT": "test"})

    assert os.environ["PERP_PLATFORM_ENVIRONMENT"] == "prod"
