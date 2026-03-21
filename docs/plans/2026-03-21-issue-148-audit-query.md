# Issue 148 Audit Query Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 为 control-plane 增加 audit event 查询接口，支持按 `event_id`、`correlation_id` 和时间窗口读取结构化审计留痕。

**Architecture:** 在 `queries.py` 中扩展 audit event read model 和 query object，在 `app.py` 中增加 `/control-plane/v1/audit/events` 路由与 query string 解析。第一版继续使用 in-memory backend，不直接连接数据库。

**Tech Stack:** Python 3.12, `dataclasses`, `urllib.parse`, `pytest`

---

### Task 1: Add failing audit query tests

**Files:**
- Create: `tests/perp_platform/control_plane/test_audit_query.py`
- Test: `tests/perp_platform/control_plane/test_audit_query.py`

**Step 1: Write the failing test**

- 覆盖：
  - audit list
  - audit detail
  - `correlation_id` filter
  - `occurred_after/occurred_before` filter
  - missing event -> `404`

**Step 2: Run test to verify it fails**

Run: `py -m pytest tests/perp_platform/control_plane/test_audit_query.py -q`

Expected:

- FAIL，因为 audit query models / handlers 尚不存在

**Step 3: Commit**

```bash
git add tests/perp_platform/control_plane/test_audit_query.py
git commit -m "test: define audit query handlers"
```

### Task 2: Implement audit query models and handlers

**Files:**
- Modify: `src/perp_platform/control_plane/queries.py`
- Modify: `src/perp_platform/control_plane/app.py`
- Modify: `src/perp_platform/control_plane/__init__.py`
- Test: `tests/perp_platform/control_plane/test_audit_query.py`
- Test: `tests/perp_platform/control_plane/test_read_models.py`

**Step 1: Add minimal implementation**

- 新增 `AuditEventView`
- 新增 `AuditEventQuery`
- 扩展 in-memory backend
- 增加 audit GET routes 与 query param parsing

**Step 2: Run targeted tests**

Run:

```bash
py -m pytest tests/perp_platform/control_plane/test_audit_query.py -q
py -m pytest tests/perp_platform/control_plane/test_read_models.py -q
```

Expected:

- PASS

**Step 3: Commit**

```bash
git add src/perp_platform/control_plane/queries.py src/perp_platform/control_plane/app.py src/perp_platform/control_plane/__init__.py tests/perp_platform/control_plane/test_audit_query.py
git commit -m "feat: add audit query endpoints"
```

### Task 3: Update docs and run full verification

**Files:**
- Modify: `README.md`
- Modify: `docs/architecture/AUDIT_LOG.md`
- Modify: `docs/plans/2026-03-21-issue-148-audit-query-design.md`
- Modify: `docs/plans/2026-03-21-issue-148-audit-query.md`

**Step 1: Update docs**

- 补充 audit query endpoints 和 filter 语义

**Step 2: Run verification**

Run:

```bash
py -m pytest tests/perp_platform/control_plane -q
py -m pytest tests -q
```

Expected:

- PASS

**Step 3: Commit**

```bash
git add README.md docs/architecture/AUDIT_LOG.md docs/plans/2026-03-21-issue-148-audit-query-design.md docs/plans/2026-03-21-issue-148-audit-query.md
git commit -m "docs: add issue 148 audit query plan"
```
