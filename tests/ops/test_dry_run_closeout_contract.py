from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
CLOSEOUT_DOC = REPO_ROOT / "docs" / "plans" / "dry-run-closeout.md"


def test_dry_run_closeout_doc_summarizes_phase_3_rehearsal() -> None:
    content = CLOSEOUT_DOC.read_text(encoding="utf-8")

    assert "repository-scoped" in content
    assert "BTC-USDT-PERP" in content
    assert "ETH-USDT-PERP" in content

    for venue in ("BYBIT", "BINANCE", "OKX"):
        assert venue in content

    assert "残余风险" in content
    assert "后续输入" in content
