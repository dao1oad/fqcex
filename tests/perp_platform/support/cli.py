from __future__ import annotations

import os
import subprocess
import sys
from contextlib import contextmanager, redirect_stdout
from dataclasses import dataclass
from io import StringIO
from typing import Iterator, Mapping, Sequence

from .config import PERP_PLATFORM_ENV_KEYS, SRC_ROOT, import_perp_platform_module


@dataclass(frozen=True)
class CLIResult:
    exit_code: int
    stdout: str


@contextmanager
def temporary_env(overrides: Mapping[str, str] | None = None) -> Iterator[None]:
    saved = {key: os.environ.get(key) for key in PERP_PLATFORM_ENV_KEYS}
    try:
        for key in PERP_PLATFORM_ENV_KEYS:
            os.environ.pop(key, None)
        if overrides is not None:
            for key, value in overrides.items():
                os.environ[key] = value
        yield
    finally:
        for key in PERP_PLATFORM_ENV_KEYS:
            os.environ.pop(key, None)
        for key, value in saved.items():
            if value is not None:
                os.environ[key] = value


def run_cli(
    args: Sequence[str] | None = None,
    *,
    env: Mapping[str, str] | None = None,
) -> CLIResult:
    cli_module = import_perp_platform_module("perp_platform.cli")
    buffer = StringIO()

    with temporary_env(env), redirect_stdout(buffer):
        exit_code = cli_module.main([] if args is None else list(args))

    return CLIResult(exit_code=exit_code, stdout=buffer.getvalue().strip())


def run_module_entrypoint(*, env: Mapping[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    command_env = os.environ.copy()
    command_env["PYTHONPATH"] = str(SRC_ROOT)
    for key in PERP_PLATFORM_ENV_KEYS:
        command_env.pop(key, None)
    if env is not None:
        command_env.update(env)

    return subprocess.run(
        [sys.executable, "-m", "perp_platform"],
        check=False,
        capture_output=True,
        text=True,
        env=command_env,
    )
