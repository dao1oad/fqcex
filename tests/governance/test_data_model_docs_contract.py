from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]


def read_text(path: str) -> str:
    return (REPO_ROOT / path).read_text(encoding="utf-8")


def test_data_model_documents_truth_fields_and_boundary_constraints() -> None:
    content = read_text("docs/architecture/DATA_MODEL.md")

    assert "Canonical quantity truth: `base_qty`" in content
    assert "Risk valuation price: `mark_price`" in content
    assert "`exchange-specific` quantity fields stay at the adapter boundary" in content
    assert "Core model truth stays venue-neutral" in content
    assert (
        "Venue conversion rules exist to normalize edge payloads into canonical truth"
        in content
    )


def test_phase1_freeze_documents_model_constraints() -> None:
    content = read_text("docs/decisions/PHASE1_FREEZE.md")

    assert "USDT linear perpetuals only" in content
    assert "position_mode = one_way" in content
    assert "margin_mode = isolated" in content
    assert "Canonical instrument for Phase 1 remains `BASE-USDT-PERP`" in content
    assert "Canonical truth quantity remains `base_qty`" in content
    assert "Venue quantity mapping stays at the adapter edge boundary" in content
    assert "Risk checks and unrealized PnL use `mark_price`" in content
    assert (
        "Exchange-specific payload fields do not enter the core model truth unchanged"
        in content
    )
