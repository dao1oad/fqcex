from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]


def read_text(path: str) -> str:
    return (REPO_ROOT / path).read_text(encoding="utf-8")


def test_contributing_documents_codex_cloud_workflow() -> None:
    content = read_text("CONTRIBUTING.md")

    assert "Codex Cloud Workflow" in content
    assert "@codex review" in content
    assert "@codex" in content
    assert "PR" in content


def test_pr_template_contains_codex_cloud_evidence_section() -> None:
    content = read_text(".github/PULL_REQUEST_TEMPLATE.md")

    assert "Codex Cloud Evidence" in content
    assert "Trigger Comment URL" in content
    assert "Codex Response URL" in content
    assert "Outcome" in content


def test_codex_cloud_dry_run_runbook_exists_with_record_section() -> None:
    content = read_text("docs/runbooks/codex-cloud-dry-run.md")

    assert "@codex" in content
    assert "Dry Run Record" in content
    assert "PR URL" in content
    assert "Trigger Comment URL" in content
    assert "Codex Response URL" in content
