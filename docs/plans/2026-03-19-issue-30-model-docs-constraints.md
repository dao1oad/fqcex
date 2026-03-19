# #30 Model Docs Constraints Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 为统一模型补齐真相字段和架构边界文档，使 `base_qty`、`mark_price`、边界层隔离和 Phase 1 冻结约束成为可验证的文档契约。

**Architecture:** 保持 doc-only 边界，修改 `docs/architecture/DATA_MODEL.md` 与 `docs/decisions/PHASE1_FREEZE.md`，并新增一个 governance 文档契约测试。测试只校验关键术语和冻结约束，不引入运行时代码改动。

**Tech Stack:** Markdown, Python 3.12, `pytest`.

---

### Task 1: 建立文档契约测试

**Files:**
- Create: `tests/governance/test_data_model_docs_contract.py`

**Step 1: Write the failing test**

```python
def test_data_model_documents_truth_fields():
    content = read_text("docs/architecture/DATA_MODEL.md")
    assert "base_qty" in content
    assert "mark_price" in content
```

**Step 2: Run test to verify it fails**

Run: `py -m pytest tests/governance/test_data_model_docs_contract.py -q`
Expected: FAIL because the current docs do not yet contain the full contract.

**Step 3: Commit**

```bash
git add tests/governance/test_data_model_docs_contract.py
git commit -m "test: add issue 30 doc contract"
```

### Task 2: 更新架构与冻结文档

**Files:**
- Modify: `docs/architecture/DATA_MODEL.md`
- Modify: `docs/decisions/PHASE1_FREEZE.md`
- Modify: `tests/governance/test_data_model_docs_contract.py`

**Step 1: Write minimal documentation update**

在 `DATA_MODEL.md` 中补齐：

- `base_qty`
- `mark_price`
- exchange-specific mapping only at edge boundary
- `one_way` / `isolated`

在 `PHASE1_FREEZE.md` 中补齐：

- `USDT` 线性永续范围
- `base_qty`
- `mark_price`
- adapter edge mapping constraint

**Step 2: Run targeted test**

Run: `py -m pytest tests/governance/test_data_model_docs_contract.py -q`
Expected: PASS

**Step 3: Run governance suite**

Run: `py -m pytest tests/governance -q`
Expected: PASS

**Step 4: Commit**

```bash
git add docs/architecture/DATA_MODEL.md docs/decisions/PHASE1_FREEZE.md tests/governance/test_data_model_docs_contract.py
git commit -m "docs: add issue 30 model constraints"
```

### Task 3: 全量验证与范围检查

**Files:**
- Verify only: `docs/architecture/DATA_MODEL.md`
- Verify only: `docs/decisions/PHASE1_FREEZE.md`
- Verify only: `tests/governance/test_data_model_docs_contract.py`
- Verify only: `docs/plans/2026-03-19-issue-30-model-docs-constraints-design.md`
- Verify only: `docs/plans/2026-03-19-issue-30-model-docs-constraints.md`

**Step 1: Verify diff scope**

Run: `git diff --stat main...HEAD`
Expected: 只包含 `DATA_MODEL.md`、`PHASE1_FREEZE.md`、governance test 和 design/plan 文档。

**Step 2: Run full test suite**

Run: `py -m pytest tests -q`
Expected: PASS

**Step 3: Commit**

```bash
git add docs/plans/2026-03-19-issue-30-model-docs-constraints-design.md docs/plans/2026-03-19-issue-30-model-docs-constraints.md
git commit -m "docs: add issue 30 design and plan"
```
