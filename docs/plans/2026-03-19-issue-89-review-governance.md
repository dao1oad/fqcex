# #89 Review Governance Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 为单账号协作补齐可审计的 review 治理最小闭环，明确 review 规则、PR 留痕格式、目录责任边界和 required checks 名称约定。

**Architecture:** 通过治理文档定义规则，通过 PR 模板收口 review 证据结构，通过 `CODEOWNERS` 表达高风险目录责任边界，并使用轻量测试验证这些契约稳定存在。当前只冻结 `governance-check` / `python-check` 名称，不实现具体 CI。

**Tech Stack:** Markdown docs, GitHub templates, `CODEOWNERS`, Python 3.12, `pytest`.

---

### Task 1: 建立 review 治理契约测试

**Files:**
- Create: `tests/governance/test_review_governance.py`

**Step 1: Write the failing test**

```python
from pathlib import Path


def test_pull_request_template_includes_review_evidence():
    content = Path(".github/PULL_REQUEST_TEMPLATE.md").read_text(encoding="utf-8")
    assert "## Review Evidence" in content
```

**Step 2: Run test to verify it fails**

Run: `py -m pytest tests/governance/test_review_governance.py -q`
Expected: FAIL because review governance sections do not exist yet.

**Step 3: Commit**

```bash
git add tests/governance/test_review_governance.py
git commit -m "test: add review governance contract"
```

### Task 2: 落地治理文档与仓库入口

**Files:**
- Modify: `GOVERNANCE.md`
- Modify: `CONTRIBUTING.md`
- Modify: `.github/PULL_REQUEST_TEMPLATE.md`
- Modify: `.github/CODEOWNERS`
- Modify: `tests/governance/test_review_governance.py`

**Step 1: Write minimal implementation**

```md
## Review Governance
...
```

```text
/.github/ @dao1oad
/docs/adr/ @dao1oad
/docs/runbooks/ @dao1oad
/docs/architecture/ @dao1oad
/src/ @dao1oad
```

**Step 2: Run targeted tests**

Run: `py -m pytest tests/governance/test_review_governance.py -q`
Expected: PASS

**Step 3: Run full tests**

Run: `py -m pytest tests -q`
Expected: PASS

**Step 4: Commit**

```bash
git add GOVERNANCE.md CONTRIBUTING.md .github/PULL_REQUEST_TEMPLATE.md .github/CODEOWNERS tests/governance/test_review_governance.py
git commit -m "docs: add single-account review governance"
```

### Task 3: 写设计与计划文档

**Files:**
- Create: `docs/plans/2026-03-19-issue-89-review-governance-design.md`
- Create: `docs/plans/2026-03-19-issue-89-review-governance.md`

**Step 1: Verify issue boundary**

Run: `git diff --stat`
Expected: 仅包含 review 治理文档、PR 模板、`CODEOWNERS` 和测试，不包含 `python-check` workflow 或平台设置变更。

**Step 2: Commit**

```bash
git add docs/plans/2026-03-19-issue-89-review-governance-design.md docs/plans/2026-03-19-issue-89-review-governance.md
git commit -m "docs: add issue 89 design and plan"
```
