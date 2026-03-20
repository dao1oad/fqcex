from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_DOC = REPO_ROOT / "docs" / "plans" / "dry-run-evidence.md"
EVIDENCE_DIR = REPO_ROOT / "docs" / "plans" / "dry-run-evidence"


def test_dry_run_evidence_doc_covers_repository_scoped_rehearsal() -> None:
    content = EVIDENCE_DOC.read_text(encoding="utf-8")

    assert "repository-scoped" in content
    assert "不是 live 或 testnet" in content
    assert "BTC-USDT-PERP" in content
    assert "ETH-USDT-PERP" in content

    for venue in ("BYBIT", "BINANCE", "OKX"):
        assert venue in content


def test_dry_run_evidence_artifacts_exist_for_btc_and_eth() -> None:
    expected_files = {
        "bybit-btc.json",
        "binance-btc.json",
        "okx-btc.json",
        "bybit-eth.json",
        "binance-eth.json",
        "okx-eth.json",
    }

    actual_files = {path.name for path in EVIDENCE_DIR.glob("*.json")}
    assert expected_files <= actual_files
