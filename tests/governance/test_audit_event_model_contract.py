from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
AUDIT_LOG_DOC = REPO_ROOT / "docs" / "architecture" / "AUDIT_LOG.md"
INCIDENT_TEMPLATE = REPO_ROOT / "docs" / "runbooks" / "incident-template.md"


def test_audit_log_doc_defines_operator_and_recovery_events() -> None:
    content = AUDIT_LOG_DOC.read_text(encoding="utf-8")

    assert "Operator Action Event" in content
    assert "Recovery Event" in content
    assert "Supervisor State Change Event" in content
    assert "event_id" in content
    assert "event_type" in content
    assert "occurred_at" in content
    assert "source_component" in content
    assert "correlation_id" in content
    assert "append-only trail" in content


def test_incident_template_references_audit_context() -> None:
    content = INCIDENT_TEMPLATE.read_text(encoding="utf-8")

    assert "Correlation ID" in content
    assert "Audit Event IDs" in content
