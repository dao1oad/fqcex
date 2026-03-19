from __future__ import annotations

from tests.perp_platform.support import run_cli, run_module_entrypoint


def test_main_returns_zero_and_prints_bootstrap_message(
) -> None:
    result = run_cli()

    assert result.exit_code == 0
    assert result.stdout == "perp-platform bootstrap ready [dev]"


def test_module_entrypoint_runs_successfully() -> None:
    result = run_module_entrypoint(env={"PERP_PLATFORM_ENVIRONMENT": "test"})

    assert result.returncode == 0
    assert result.stdout.strip() == "perp-platform bootstrap ready [test]"
