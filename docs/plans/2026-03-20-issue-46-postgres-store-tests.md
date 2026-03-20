# Issue 46 PostgreSQL Store Integration Tests And Initialization Docs Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 为 PostgreSQL truth store 增加高层 contract test，并补齐初始化与持久化映射文档。

**Architecture:** 不引入真实数据库；继续沿用 schema constants 与 repository SQL builder contract，通过高层测试验证 schema、repositories、canonical fields 和初始化文档一致。

**Tech Stack:** Python 3.12、pytest、Markdown

---

### Task 1: Add failing store contract tests

**Files:**
- Create: `tests/perp_platform/store/test_postgres_store.py`

**Step 1: Write the failing tests**

- 验证 store package 暴露 schema 与 repository 符号
- 验证 schema 表集覆盖 repository contract
- 验证 canonical fields 同时存在于 schema / repository contract

**Step 2: Run targeted test to verify failure**

Run:

```bash
py -m pytest tests/perp_platform/store/test_postgres_store.py -q
```

Expected:
- FAIL，因为测试文件和部分文档断言尚未存在

**Step 3: Commit**

```bash
git add tests/perp_platform/store/test_postgres_store.py
git commit -m "test: define postgres store integration contract"
```

### Task 2: Update truth-store documentation and package exports

**Files:**
- Modify: `docs/architecture/DATA_MODEL.md`
- Modify: `src/perp_platform/store/__init__.py`
- Modify: `src/perp_platform/store/postgres/__init__.py`
- Test: `tests/perp_platform/store/test_postgres_store.py`

**Step 1: Write minimal implementation**

- 暴露 store / postgres package 的最小入口
- 在 `DATA_MODEL.md` 增加初始化与持久化映射说明

**Step 2: Run targeted tests**

Run:

```bash
py -m pytest tests/perp_platform/store/test_postgres_store.py -q
```

Expected:
- PASS

**Step 3: Commit**

```bash
git add docs/architecture/DATA_MODEL.md src/perp_platform/store/__init__.py src/perp_platform/store/postgres/__init__.py tests/perp_platform/store/test_postgres_store.py
git commit -m "feat: document postgres store initialization"
```

### Task 3: Verify full store scope

**Files:**
- Verify only

**Step 1: Run store verification**

Run:

```bash
py -m pytest tests/perp_platform/store -q
```

Expected:
- PASS

**Step 2: Run full regression**

Run:

```bash
py -m pytest tests -q
```

Expected:
- PASS

**Step 3: Commit**

```bash
git add docs/plans/2026-03-20-issue-46-postgres-store-tests-design.md docs/plans/2026-03-20-issue-46-postgres-store-tests.md
git commit -m "docs: add issue 46 postgres store plan"
```
