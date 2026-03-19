# #81 perp-platform CI Workflow Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 为 `perp_platform` 建立最小 Python CI 护栏，在保留 `governance-check` 的同时新增 `python-check`，并让仓库入口文档与当前 CI 行为一致。

**Architecture:** 继续沿用单个 GitHub Actions workflow，在现有 `ci.yml` 上增量添加 `python-check`，通过 `pip install -e .` 和 `pytest tests -q` 验证包安装与全量测试链路；同时更新 `README.md` 说明当前最小 CI 边界。使用轻量契约测试验证 workflow 和文档中的关键 token。

**Tech Stack:** GitHub Actions YAML, Markdown, Python 3.12, `pytest`.

---

### Task 1: 建立 CI 契约测试

**Files:**
- Create: `tests/governance/test_ci_workflow_contract.py`

**Step 1: Write the failing test**

```python
from pathlib import Path


def test_ci_workflow_defines_python_check():
    content = Path(".github/workflows/ci.yml").read_text(encoding="utf-8")
    assert "python-check:" in content
```

**Step 2: Run test to verify it fails**

Run: `py -m pytest tests/governance/test_ci_workflow_contract.py -q`
Expected: FAIL because the current workflow only contains `governance-check`.

**Step 3: Commit**

```bash
git add tests/governance/test_ci_workflow_contract.py
git commit -m "test: add ci workflow contract"
```

### Task 2: 实现最小 Python CI 与 README 说明

**Files:**
- Modify: `.github/workflows/ci.yml`
- Modify: `README.md`
- Modify: `tests/governance/test_ci_workflow_contract.py`

**Step 1: Write minimal implementation**

```yaml
  python-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: python -m pip install --upgrade pip
      - run: python -m pip install -e .
      - run: python -m pytest tests -q
```

```md
## CI

- `governance-check`
- `python-check`
```

**Step 2: Run targeted tests**

Run: `py -m pytest tests/governance/test_ci_workflow_contract.py -q`
Expected: PASS

**Step 3: Run full tests**

Run: `py -m pytest tests -q`
Expected: PASS

**Step 4: Commit**

```bash
git add .github/workflows/ci.yml README.md tests/governance/test_ci_workflow_contract.py
git commit -m "ci: add perp-platform python checks"
```

### Task 3: 边界回归检查

**Files:**
- Verify only: `.github/workflows/ci.yml`
- Verify only: `README.md`
- Verify only: `docs/plans/2026-03-19-issue-81-perp-platform-ci-workflow-design.md`
- Verify only: `docs/plans/2026-03-19-issue-81-perp-platform-ci-workflow.md`

**Step 1: Verify diff scope**

Run: `git diff --stat main...HEAD`
Expected: 只包含 CI workflow、README、设计/计划文档和 CI 契约测试，不包含 Docker、deploy、smoke 或平台设置变更。

**Step 2: Final verification**

Run: `py -m pytest tests -q`
Expected: PASS

**Step 3: Commit**

```bash
git add docs/plans/2026-03-19-issue-81-perp-platform-ci-workflow-design.md docs/plans/2026-03-19-issue-81-perp-platform-ci-workflow.md
git commit -m "docs: add issue 81 design and plan"
```
