from pathlib import Path


def test_issue_orchestrator_runbook_mentions_single_writer_and_gpt_5_4_xhigh() -> None:
    runbook_path = Path("docs/runbooks/issue-orchestrator.md")
    content = runbook_path.read_text(encoding="utf-8")

    assert "single writer" in content
    assert "gpt-5.4" in content
    assert "xhigh" in content
    assert "approval bundle" in content
    assert "gh sync" in content
    assert "start" in content
    assert "fail closed" in content
