from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
SECURITY_DOC = REPO_ROOT / "SECURITY.md"
AUDIT_LOG_DOC = REPO_ROOT / "docs" / "architecture" / "AUDIT_LOG.md"
FORCE_RESUME_POLICY = REPO_ROOT / "docs" / "runbooks" / "force-resume-policy.md"


def test_security_doc_defines_audit_retention_redaction_and_access_rules() -> None:
    content = SECURITY_DOC.read_text(encoding="utf-8")

    assert "Audit Data Governance" in content
    assert "365 days" in content
    assert "redact account identifiers" in content
    assert "named operators" in content
    assert "developers receive redacted audit views" in content


def test_audit_log_doc_defines_retention_and_redaction_rules() -> None:
    content = AUDIT_LOG_DOC.read_text(encoding="utf-8")

    assert "Retention Policy" in content
    assert "Redaction Rules" in content
    assert "Access Boundary" in content


def test_force_resume_policy_requires_redacted_operator_evidence() -> None:
    content = FORCE_RESUME_POLICY.read_text(encoding="utf-8")

    assert "Evidence Hygiene" in content
    assert "redact account identifiers" in content
    assert "redact credentials" in content
