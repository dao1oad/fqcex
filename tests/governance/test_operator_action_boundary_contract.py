from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
CONTROL_PLANE_API = REPO_ROOT / "docs" / "architecture" / "control-plane-api.md"
FORCE_RESUME_POLICY = REPO_ROOT / "docs" / "runbooks" / "force-resume-policy.md"
SECURITY_DOC = REPO_ROOT / "SECURITY.md"


def test_control_plane_api_defines_operator_action_boundary() -> None:
    content = CONTROL_PLANE_API.read_text(encoding="utf-8")

    assert "Action Permission Boundary" in content
    assert "read-only clients" in content
    assert "named human operator" in content
    assert "force_resume" in content
    assert "cannot bypass unresolved recovery or reconciliation prerequisites" in content


def test_force_resume_policy_requires_explicit_human_approval() -> None:
    content = FORCE_RESUME_POLICY.read_text(encoding="utf-8")

    assert "Permission Boundary" in content
    assert "named human operator" in content
    assert "Codex cloud" in content
    assert "latest recovery context" in content


def test_security_doc_prohibits_control_plane_write_credentials_in_cloud() -> None:
    content = SECURITY_DOC.read_text(encoding="utf-8")

    assert "control-plane write tokens" in content
    assert "human-scoped identities" in content
    assert "must not be placed into Codex cloud environments" in content
