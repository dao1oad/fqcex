# Issue 58 Checker Signals Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 把 checker policy 结果投影成 `Supervisor` 可消费的状态建议信号，并补齐对应测试。

**Architecture:** 新增 `src/perp_platform/checker/signals.py`，输入 `CheckerPolicyResult` 输出 `CheckerSupervisorSignal`。映射只使用现有 `SupervisorState`，不改动 Supervisor truth ownership 或 trigger contract。healthy 映射到 `LIVE`，stale 映射到 `DEGRADED`，diverged 映射到 `RESYNCING`，同时存在时取更严格状态。

**Tech Stack:** Python 3.12, dataclasses, Decimal, pytest

---

### Task 1: Add failing checker signal tests

**Files:**
- Create: `tests/perp_platform/test_checker_signals.py`

**Step 1: Write the failing test**

覆盖：

- healthy -> `LIVE`
- stale -> `DEGRADED`
- diverged -> `RESYNCING`
- stale + diverged -> `RESYNCING`

**Step 2: Run test to verify it fails**

Run: `py -m pytest tests/perp_platform/test_checker_signals.py -q`

Expected: FAIL because `perp_platform.checker.signals` does not exist yet.

**Step 3: Commit**

```bash
git add tests/perp_platform/test_checker_signals.py
git commit -m "test: add failing checker signal tests"
```

### Task 2: Implement signal projection

**Files:**
- Create: `src/perp_platform/checker/signals.py`
- Modify: `src/perp_platform/checker/__init__.py`
- Test: `tests/perp_platform/test_checker_signals.py`

**Step 1: Write minimal implementation**

实现：

- `CheckerSupervisorSignal`
- `build_checker_supervisor_signal(...)`
- reason constants for healthy / stale / divergence

**Step 2: Run targeted test**

Run: `py -m pytest tests/perp_platform/test_checker_signals.py -q`

Expected: PASS

**Step 3: Commit**

```bash
git add src/perp_platform/checker/signals.py src/perp_platform/checker/__init__.py tests/perp_platform/test_checker_signals.py
git commit -m "feat: add checker supervisor signals"
```

### Task 3: Document checker signal boundary

**Files:**
- Modify: `docs/architecture/ARCHITECTURE.md`

**Step 1: Add architecture note**

补充：

- checker policy first becomes a supervisor-consumable signal
- signal carries suggested state only
- Supervisor remains the tradeability truth source

**Step 2: Re-run targeted test**

Run: `py -m pytest tests/perp_platform/test_checker_signals.py -q`

Expected: PASS

**Step 3: Commit**

```bash
git add docs/architecture/ARCHITECTURE.md
git commit -m "docs: add checker signal architecture note"
```

### Task 4: Verify end to end

**Files:**
- Modify: `docs/plans/2026-03-20-issue-58-checker-signals-design.md`
- Modify: `docs/plans/2026-03-20-issue-58-checker-signals.md`

**Step 1: Run checker targeted tests**

Run: `py -m pytest tests/perp_platform/test_checker_policies.py tests/perp_platform/test_checker_signals.py -q`

Expected: PASS

**Step 2: Run package tests**

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
git add src/perp_platform/checker/__init__.py src/perp_platform/checker/signals.py tests/perp_platform/test_checker_signals.py docs/architecture/ARCHITECTURE.md docs/plans/2026-03-20-issue-58-checker-signals-design.md docs/plans/2026-03-20-issue-58-checker-signals.md
git commit -m "feat: add checker supervisor signal mapping"
```
