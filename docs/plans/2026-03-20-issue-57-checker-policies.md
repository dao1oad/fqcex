# Issue 57 Checker Policies Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 为 checker 增加最小的新鲜度与顶档偏差策略层，产出后续 `#58` 可消费的统一评估结果。

**Architecture:** 在 `src/perp_platform/checker/policies.py` 中新增独立策略输入、阈值和结果模型，策略仅判断 freshness 与 divergence，不直接投影到 Supervisor。默认阈值固定在代码中，freshness 基于 `receipt_timestamp`，divergence 基于同 venue / instrument bid/ask 相对偏差。

**Tech Stack:** Python 3.12, dataclasses, Decimal, pytest

---

### Task 1: Add failing checker policy tests

**Files:**
- Create: `tests/perp_platform/test_checker_policies.py`

**Step 1: Write the failing test**

覆盖：

- freshness healthy
- freshness stale
- divergence healthy
- divergence breached
- mismatched venue / instrument rejected

**Step 2: Run test to verify it fails**

Run: `py -m pytest tests/perp_platform/test_checker_policies.py -q`

Expected: FAIL because `perp_platform.checker.policies` does not exist yet.

**Step 3: Commit**

```bash
git add tests/perp_platform/test_checker_policies.py
git commit -m "test: add failing checker policy tests"
```

### Task 2: Implement policy models and evaluation

**Files:**
- Create: `src/perp_platform/checker/policies.py`
- Modify: `src/perp_platform/checker/__init__.py`
- Test: `tests/perp_platform/test_checker_policies.py`

**Step 1: Write minimal implementation**

实现：

- `CheckerReferenceTopOfBook`
- `CheckerPolicyThresholds`
- `CheckerPolicyResult`
- `DEFAULT_CHECKER_POLICY_THRESHOLDS`
- `evaluate_checker_policies(...)`

并在内部完成：

- `age_seconds` 计算
- bid/ask divergence bps 计算
- stale / diverged 判定
- venue / instrument mismatch fail closed

**Step 2: Run targeted test**

Run: `py -m pytest tests/perp_platform/test_checker_policies.py -q`

Expected: PASS

**Step 3: Commit**

```bash
git add src/perp_platform/checker/policies.py src/perp_platform/checker/__init__.py tests/perp_platform/test_checker_policies.py
git commit -m "feat: add checker policy evaluation"
```

### Task 3: Document checker policy boundary

**Files:**
- Modify: `docs/architecture/ARCHITECTURE.md`

**Step 1: Add architecture note**

补充：

- freshness uses `receipt_timestamp`
- divergence compares same-venue same-instrument bid/ask in basis points
- policy layer emits judgments only and does not overwrite Supervisor truth

**Step 2: Run targeted test again**

Run: `py -m pytest tests/perp_platform/test_checker_policies.py -q`

Expected: PASS

**Step 3: Commit**

```bash
git add docs/architecture/ARCHITECTURE.md
git commit -m "docs: add checker policy boundary note"
```

### Task 4: Verify branch end to end

**Files:**
- Modify: `docs/plans/2026-03-20-issue-57-checker-policies-design.md`
- Modify: `docs/plans/2026-03-20-issue-57-checker-policies.md`

**Step 1: Run checker-targeted tests**

Run: `py -m pytest tests/perp_platform/test_checker_policies.py -q`

Expected: PASS

**Step 2: Run broader package tests**

Run: `py -m pytest tests/perp_platform -q`

Expected: PASS

**Step 3: Run full test suite**

Run: `py -m pytest tests -q`

Expected: PASS

**Step 4: Run editable install verification**

Run: `py -m pip install -e .`

Expected: success

**Step 5: Final commit**

```bash
git add src/perp_platform/checker/__init__.py src/perp_platform/checker/policies.py tests/perp_platform/test_checker_policies.py docs/architecture/ARCHITECTURE.md docs/plans/2026-03-20-issue-57-checker-policies-design.md docs/plans/2026-03-20-issue-57-checker-policies.md
git commit -m "feat: add checker freshness and divergence policies"
```
