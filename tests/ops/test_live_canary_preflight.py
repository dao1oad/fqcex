from __future__ import annotations

from pathlib import Path
from subprocess import run
import sys


REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT_PATH = REPO_ROOT / "scripts" / "live_canary_preflight.py"


def write_live_env(
    env_path: Path,
    *,
    allowed_venues: str = "BYBIT,BINANCE,OKX",
    allowed_instruments: str = "BTC-USDT-PERP,ETH-USDT-PERP",
    bybit_credentials: str = "secrets/bybit.env",
    binance_credentials: str = "secrets/binance.env",
    okx_credentials: str = "secrets/okx.env",
    kill_switch_path: str = "state/kill-switch.flag",
) -> None:
    env_path.write_text(
        "\n".join(
            [
                "PERP_PLATFORM_APP_NAME=perp-platform-live-canary",
                "PERP_PLATFORM_ENVIRONMENT=live-canary",
                "PERP_PLATFORM_LOG_LEVEL=INFO",
                "PERP_PLATFORM_IMAGE_REPO=perp-platform",
                "PERP_PLATFORM_IMAGE_TAG=latest",
                "LIVE_CANARY_ENABLED=true",
                f"LIVE_CANARY_ALLOWED_VENUES={allowed_venues}",
                f"LIVE_CANARY_ALLOWED_INSTRUMENTS={allowed_instruments}",
                "LIVE_CANARY_MAX_NOTIONAL_USD=250",
                f"LIVE_CANARY_KILL_SWITCH_PATH={kill_switch_path}",
                f"BYBIT_CREDENTIALS_FILE={bybit_credentials}",
                f"BINANCE_CREDENTIALS_FILE={binance_credentials}",
                f"OKX_CREDENTIALS_FILE={okx_credentials}",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def run_preflight(env_path: Path) -> tuple[int, str, str]:
    result = run(
        [sys.executable, str(SCRIPT_PATH), "--env-file", str(env_path)],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    return result.returncode, result.stdout, result.stderr


def test_live_canary_preflight_passes_with_valid_env(tmp_path: Path) -> None:
    env_path = tmp_path / "live.env"
    secrets_dir = tmp_path / "secrets"
    state_dir = tmp_path / "state"
    secrets_dir.mkdir()
    state_dir.mkdir()
    (secrets_dir / "bybit.env").write_text("key=value\n", encoding="utf-8")
    (secrets_dir / "binance.env").write_text("key=value\n", encoding="utf-8")
    (secrets_dir / "okx.env").write_text("key=value\n", encoding="utf-8")
    (state_dir / "kill-switch.flag").write_text("armed=false\n", encoding="utf-8")
    write_live_env(
        env_path,
        bybit_credentials=str(secrets_dir / "bybit.env"),
        binance_credentials=str(secrets_dir / "binance.env"),
        okx_credentials=str(secrets_dir / "okx.env"),
        kill_switch_path=str(state_dir / "kill-switch.flag"),
    )

    returncode, stdout, stderr = run_preflight(env_path)

    assert returncode == 0, stderr
    assert "live canary preflight passed" in stdout


def test_live_canary_preflight_blocks_missing_credentials_file(tmp_path: Path) -> None:
    env_path = tmp_path / "live.env"
    state_dir = tmp_path / "state"
    state_dir.mkdir()
    (state_dir / "kill-switch.flag").write_text("armed=false\n", encoding="utf-8")
    write_live_env(
        env_path,
        bybit_credentials=str(tmp_path / "missing-bybit.env"),
        binance_credentials=str(tmp_path / "missing-binance.env"),
        okx_credentials=str(tmp_path / "missing-okx.env"),
        kill_switch_path=str(state_dir / "kill-switch.flag"),
    )

    returncode, _stdout, stderr = run_preflight(env_path)

    assert returncode == 1
    assert "missing credentials file" in stderr


def test_live_canary_preflight_blocks_missing_allowlist(tmp_path: Path) -> None:
    env_path = tmp_path / "live.env"
    secrets_dir = tmp_path / "secrets"
    state_dir = tmp_path / "state"
    secrets_dir.mkdir()
    state_dir.mkdir()
    (secrets_dir / "bybit.env").write_text("key=value\n", encoding="utf-8")
    (secrets_dir / "binance.env").write_text("key=value\n", encoding="utf-8")
    (secrets_dir / "okx.env").write_text("key=value\n", encoding="utf-8")
    (state_dir / "kill-switch.flag").write_text("armed=false\n", encoding="utf-8")
    write_live_env(
        env_path,
        allowed_instruments="",
        bybit_credentials=str(secrets_dir / "bybit.env"),
        binance_credentials=str(secrets_dir / "binance.env"),
        okx_credentials=str(secrets_dir / "okx.env"),
        kill_switch_path=str(state_dir / "kill-switch.flag"),
    )

    returncode, _stdout, stderr = run_preflight(env_path)

    assert returncode == 1
    assert "missing live canary instrument allowlist" in stderr


def test_live_canary_preflight_blocks_missing_kill_switch_file(tmp_path: Path) -> None:
    env_path = tmp_path / "live.env"
    secrets_dir = tmp_path / "secrets"
    secrets_dir.mkdir()
    (secrets_dir / "bybit.env").write_text("key=value\n", encoding="utf-8")
    (secrets_dir / "binance.env").write_text("key=value\n", encoding="utf-8")
    (secrets_dir / "okx.env").write_text("key=value\n", encoding="utf-8")
    write_live_env(
        env_path,
        bybit_credentials=str(secrets_dir / "bybit.env"),
        binance_credentials=str(secrets_dir / "binance.env"),
        okx_credentials=str(secrets_dir / "okx.env"),
        kill_switch_path=str(tmp_path / "state" / "kill-switch.flag"),
    )

    returncode, _stdout, stderr = run_preflight(env_path)

    assert returncode == 1
    assert "missing kill switch file" in stderr
