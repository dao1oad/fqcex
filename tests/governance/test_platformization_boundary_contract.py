from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
ARCHITECTURE_DOC = REPO_ROOT / "docs" / "architecture" / "ARCHITECTURE.md"
ROADMAP_DOC = REPO_ROOT / "docs" / "roadmap" / "ROADMAP.md"


def test_architecture_doc_defines_platformization_boundary_and_migration_plan() -> None:
    content = ARCHITECTURE_DOC.read_text(encoding="utf-8")

    assert "Platformization Boundary" in content
    assert "Migration Plan" in content
    assert "Control Plane remains projection-only" in content
    assert "Supervisor remains the tradeability truth source" in content


def test_roadmap_doc_lists_phase_4_delivery_order() -> None:
    content = ROADMAP_DOC.read_text(encoding="utf-8")

    assert "Phase 4 Delivery Order" in content
    assert "control-plane api surface" in content
    assert "operator actions and permissions" in content
    assert "audit boundary and runbooks" in content
