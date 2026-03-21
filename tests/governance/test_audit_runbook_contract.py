from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
AUDIT_CHECKLIST = REPO_ROOT / "docs" / "runbooks" / "audit-checklist.md"
INCIDENT_TEMPLATE = REPO_ROOT / "docs" / "runbooks" / "incident-template.md"
FORCE_RESUME_POLICY = REPO_ROOT / "docs" / "runbooks" / "force-resume-policy.md"


def test_audit_checklist_exists_with_minimal_acceptance_sections() -> None:
    content = AUDIT_CHECKLIST.read_text(encoding="utf-8")

    assert "Manual Unblock Pre-Check" in content
    assert "Event Replay" in content
    assert "Evidence Retention" in content
    assert "Audit Reconciliation" in content


def test_incident_template_references_audit_checklist() -> None:
    content = INCIDENT_TEMPLATE.read_text(encoding="utf-8")

    assert "Audit Checklist" in content
    assert "docs/runbooks/audit-checklist.md" in content


def test_force_resume_policy_references_audit_checklist() -> None:
    content = FORCE_RESUME_POLICY.read_text(encoding="utf-8")

    assert "Audit Checklist" in content
    assert "docs/runbooks/audit-checklist.md" in content
