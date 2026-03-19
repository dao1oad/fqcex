from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]


def read_text(path: str) -> str:
    return (REPO_ROOT / path).read_text(encoding="utf-8")


def test_governance_defines_review_governance() -> None:
    content = read_text("GOVERNANCE.md")

    assert "## 6. Review Governance" in content
    assert "single-account" in content
    assert "governance-check" in content
    assert "python-check" in content


def test_contributing_documents_review_requirements() -> None:
    content = read_text("CONTRIBUTING.md")

    assert "## Review Requirements" in content
    assert "Review Evidence" in content
    assert "independent review comment" in content


def test_pull_request_template_includes_review_evidence() -> None:
    content = read_text(".github/PULL_REQUEST_TEMPLATE.md")

    assert "## Review Evidence" in content
    assert "Base SHA" in content
    assert "Head SHA" in content
    assert "Final Verification" in content


def test_codeowners_covers_high_risk_paths() -> None:
    content = read_text(".github/CODEOWNERS")

    assert "/.github/ @dao1oad" in content
    assert "/docs/adr/ @dao1oad" in content
    assert "/docs/runbooks/ @dao1oad" in content
    assert "/docs/architecture/ @dao1oad" in content
    assert "/src/ @dao1oad" in content
