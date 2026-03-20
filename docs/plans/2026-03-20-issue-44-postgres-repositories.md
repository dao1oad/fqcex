# Issue 44 PostgreSQL Repositories Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 为订单、仓位、余额增加 driver-agnostic PostgreSQL repository contract。

**Architecture:** repository 负责把 canonical record 编译成 `PostgresStatement(sql, params)`，不负责连接和执行。

**Tech Stack:** Python 3.12、dataclasses、pytest

---

### Task 1: Add failing repository contract tests

**Files:**
- Create: `tests/perp_platform/store/test_postgres_repositories.py`

**Step 1: Write the failing tests**

- orders / positions / balances repository 的 upsert SQL
- select-for-account SQL
- params 字典保持输入字段

**Step 2: Run targeted tests to verify failure**

Run:

```bash
py -m pytest tests/perp_platform/store/test_postgres_repositories.py -q
```

Expected:
- FAIL，因为 repositories 尚不存在

**Step 3: Commit**

```bash
git add tests/perp_platform/store/test_postgres_repositories.py
git commit -m "test: define postgres repository contracts"
```

### Task 2: Implement repository statement builders

**Files:**
- Create: `src/perp_platform/store/postgres/repositories/__init__.py`
- Create: `src/perp_platform/store/postgres/repositories/base.py`
- Create: `src/perp_platform/store/postgres/repositories/orders.py`
- Create: `src/perp_platform/store/postgres/repositories/positions.py`
- Create: `src/perp_platform/store/postgres/repositories/balances.py`
- Test: `tests/perp_platform/store/test_postgres_repositories.py`

**Step 1: Write minimal implementation**

- 新增 `PostgresStatement`
- 新增三个 record dataclass
- 新增三个 repository builder 类

**Step 2: Run targeted tests**

Run:

```bash
py -m pytest tests/perp_platform/store/test_postgres_repositories.py -q
```

Expected:
- PASS

**Step 3: Commit**

```bash
git add src/perp_platform/store/postgres/repositories/__init__.py src/perp_platform/store/postgres/repositories/base.py src/perp_platform/store/postgres/repositories/orders.py src/perp_platform/store/postgres/repositories/positions.py src/perp_platform/store/postgres/repositories/balances.py tests/perp_platform/store/test_postgres_repositories.py
git commit -m "feat: add postgres truth repositories"
```

### Task 3: Verify full scope and prepare merge

**Files:**
- Modify: `docs/plans/2026-03-20-issue-44-postgres-repositories-design.md`
- Modify: `docs/plans/2026-03-20-issue-44-postgres-repositories.md`

**Step 1: Run verification**

Run:

```bash
py -m pytest tests/perp_platform/store/test_postgres_repositories.py -q
py -m pytest tests -q
```

Expected:
- 全部 PASS

**Step 2: Confirm scope**

- 仅新增 orders / positions / balances repository contract
- 没有 tradeability / recovery repository
- 没有 DB driver

**Step 3: Commit**

```bash
git add docs/plans/2026-03-20-issue-44-postgres-repositories-design.md docs/plans/2026-03-20-issue-44-postgres-repositories.md
git commit -m "docs: add issue 44 postgres repository plan"
```
