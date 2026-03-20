# Issue 43 PostgreSQL Core Schema Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 为 PostgreSQL 真相存储增加最小核心 schema 和初始 migration，给后续 repository 实现提供稳定表结构。

**Architecture:** 使用纯 SQL migration + Python schema 常量模块；不引入 ORM 或数据库驱动。

**Tech Stack:** Python 3.12、SQL、pytest

---

### Task 1: Add failing schema contract tests

**Files:**
- Create: `tests/perp_platform/store/test_postgres_schema.py`

**Step 1: Write the failing tests**

- schema 模块可导入
- `CORE_TRUTH_TABLES` 含 9 张表
- migration 文件存在
- migration 文件含关键表和字段

**Step 2: Run targeted tests to verify failure**

Run:

```bash
py -m pytest tests/perp_platform/store/test_postgres_schema.py -q
```

Expected:
- FAIL，因为 `store/postgres/schema.py` 和 migration 尚不存在

**Step 3: Commit**

```bash
git add tests/perp_platform/store/test_postgres_schema.py
git commit -m "test: define postgres schema contract"
```

### Task 2: Implement schema module and migration

**Files:**
- Create: `migrations/postgres/0001_core_truth_schema.sql`
- Create: `src/perp_platform/store/__init__.py`
- Create: `src/perp_platform/store/postgres/__init__.py`
- Create: `src/perp_platform/store/postgres/schema.py`
- Test: `tests/perp_platform/store/test_postgres_schema.py`

**Step 1: Write minimal implementation**

- 新增 9 张核心表的初始 migration
- 新增 Python schema 常量与版本号

**Step 2: Run targeted tests**

Run:

```bash
py -m pytest tests/perp_platform/store/test_postgres_schema.py -q
```

Expected:
- PASS

**Step 3: Commit**

```bash
git add migrations/postgres/0001_core_truth_schema.sql src/perp_platform/store/__init__.py src/perp_platform/store/postgres/__init__.py src/perp_platform/store/postgres/schema.py tests/perp_platform/store/test_postgres_schema.py
git commit -m "feat: add postgres core schema"
```

### Task 3: Verify full scope and prepare merge

**Files:**
- Modify: `docs/plans/2026-03-20-issue-43-postgres-schema-design.md`
- Modify: `docs/plans/2026-03-20-issue-43-postgres-schema.md`

**Step 1: Run verification**

Run:

```bash
py -m pytest tests/perp_platform/store/test_postgres_schema.py -q
py -m pytest tests -q
```

Expected:
- 全部 PASS

**Step 2: Confirm scope**

- 仅新增 schema / migration / contract tests
- 未引入 DB driver 或 repository

**Step 3: Commit**

```bash
git add docs/plans/2026-03-20-issue-43-postgres-schema-design.md docs/plans/2026-03-20-issue-43-postgres-schema.md
git commit -m "docs: add issue 43 postgres schema plan"
```
