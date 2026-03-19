from __future__ import annotations

import os

from .config import load_config


def main(argv: list[str] | None = None) -> int:
    _ = [] if argv is None else list(argv)
    config = load_config(os.environ)
    print(f"{config.app_name} bootstrap ready [{config.environment}]")
    return 0
