# Issue 45 PostgreSQL Tradeability And Recovery Repositories Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 为 tradeability 和 recovery 增加 driver-agnostic PostgreSQL repository contract。

**Architecture:** 继续沿用 `PostgresStatement(sql, params)` 方案；tradeability 用 upsert/select，recovery 用 start / complete / recent-runs statement builders。

**Tech Stack:** Python 3.12、dataclasses、pytest

---

### Task 1: Add failing tradeability/recovery repository tests

**Files:**
- Create: `tests/perp_platform/store/test_postgres_tradeability_recovery.py`

**Step 1: Write the failing tests**

- tradeability upsert/select contract
- recovery start/complete/select contract

**Step 2: Run targeted tests to verify failure**

Run:

```bash
py -m pytest tests/perp_platform/store/test_postgres_tradeability_recovery.py -q
```

Expected:
- FAIL，因为 repositories 尚不存在

**Step 3: Commit**

```bash
git add tests/perp_platform/store/test_postgres_tradeability_recovery.py
git commit -m "test: define postgres tradeability and recovery repositories"
```

### Task 2: Implement repository statement builders

**Files:**
- Create: `src/perp_platform/store/postgres/repositories/tradeability.py`
- Create: `src/perp_platform/store/postgres/repositories/recovery.py`
- Modify: `src/perp_platform/store/postgres/repositories/__init__.py`
- Test: `tests/perp_platform/store/test_postgres_tradeability_recovery.py`

**Step 1: Write minimal implementation**

- 新增 tradeability / recovery record dataclass
- 新增 repository builder 类
- 导出相关符号

**Step 2: Run targeted tests**

Run:

```bash
py -m pytest tests/perp_platform/store/test_postgres_tradeability_recovery.py -q
```

Expected:
- PASS

**Step 3: Commit**

```bash
git add src/perp_platform/store/postgres/repositories/tradeability.py src/perp_platform/store/postgres/repositories/recovery.py src/perp_platform/store/postgres/repositories/__init__.py tests/perp_platform/store/test_postgres_tradeability_recovery.py
git commit -m "feat: add postgres tradeability and recovery repositories"
```

### Task 3: Verify full scope and prepare merge

**Files:**
- Modify: `docs/plans/2026-03-20-issue-45-postgres-tradeability-recovery-design.md`
- Modify: `docs/plans/2026-03-20-issue-45-postgres-tradeability-recovery.md`

**Step 1: Run verification**

Run:

```bash
py -m pytest tests/perp_platform/store/test_postgres_tradeability_recovery.py -q
py -m pytest tests -q
```

Expected:
- 全部 PASS

**Step 2: Confirm scope**

- 仅新增 tradeability / recovery repository
- 没有 DB driver
- 没有 integration test

**Step 3: Commit**

```bash
git add docs/plans/2026-03-20-issue-45-postgres-tradeability-recovery-design.md docs/plans/2026-03-20-issue-45-postgres-tradeability-recovery.md
git commit -m "docs: add issue 45 postgres repository plan"
```
