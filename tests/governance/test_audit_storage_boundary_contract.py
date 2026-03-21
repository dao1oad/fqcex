from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
AUDIT_LOG_DOC = REPO_ROOT / "docs" / "architecture" / "AUDIT_LOG.md"
DATA_MODEL_DOC = REPO_ROOT / "docs" / "architecture" / "DATA_MODEL.md"
CONTROL_PLANE_API = REPO_ROOT / "docs" / "architecture" / "control-plane-api.md"


def test_audit_log_doc_defines_persistence_and_query_boundaries() -> None:
    content = AUDIT_LOG_DOC.read_text(encoding="utf-8")

    assert "Persistence Boundary" in content
    assert "Query Boundary" in content
    assert "append-only PostgreSQL audit store" in content
    assert "incident narratives remain outside PostgreSQL" in content


def test_data_model_doc_maps_audit_events_without_changing_truth_ownership() -> None:
    content = DATA_MODEL_DOC.read_text(encoding="utf-8")

    assert "Audit Storage Boundary" in content
    assert "`audit_events`" in content
    assert "not part of the core trading truth tables" in content


def test_control_plane_api_exposes_read_only_audit_query_surface() -> None:
    content = CONTROL_PLANE_API.read_text(encoding="utf-8")

    assert "Audit Events" in content
    assert "GET /control-plane/v1/audit/events" in content
    assert "read-only audit query surface" in content
