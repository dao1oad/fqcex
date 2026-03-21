# Issue 162 Audit Query Hardening Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 修复 audit query 的默认脱敏边界、RFC3339 时间窗口过滤语义和非法时间参数校验。

**Architecture:** 保持 `AuditEventView` 作为内部 read model，在 control-plane 序列化层输出 redacted shared view；查询参数和 event timestamp 都统一解析成 aware `datetime` 后比较，并把非法 query 参数收口成 `400 invalid_request`。

**Tech Stack:** Python 3.12, `datetime`, `pytest`

---

### Task 1: Add failing regression tests for redaction and time validation

**Files:**
- Modify: `tests/perp_platform/control_plane/test_audit_query.py`
- Test: `tests/perp_platform/control_plane/test_audit_query.py`

**Step 1: Write the failing test**

- 覆盖：
  - `recorded_by` 默认 redacted
  - 非 allowlist scope key 不暴露
  - `+08:00` / `Z` 时间窗口比较正确
  - 非法时间参数返回 `400 invalid_request`

**Step 2: Run test to verify it fails**

Run: `py -m pytest tests/perp_platform/control_plane/test_audit_query.py -q`

Expected:

- FAIL，因为当前主线没有 redaction 和时间校验

**Step 3: Commit**

```bash
git add tests/perp_platform/control_plane/test_audit_query.py
git commit -m "test: add audit query hardening coverage"
```

### Task 2: Implement redacted serialization and RFC3339 filtering

**Files:**
- Modify: `src/perp_platform/control_plane/queries.py`
- Modify: `src/perp_platform/control_plane/app.py`
- Modify: `src/perp_platform/control_plane/__init__.py`
- Test: `tests/perp_platform/control_plane/test_audit_query.py`

**Step 1: Add minimal implementation**

- 新增 audit-specific serialization helper
- 默认 redacted `recorded_by`
- 裁剪 `scope`
- 解析/比较 RFC3339 时间戳
- 非法时间 query 返回 `invalid_request`

**Step 2: Run targeted tests**

Run:

```bash
py -m pytest tests/perp_platform/control_plane/test_audit_query.py -q
py -m pytest tests/perp_platform/control_plane -q
```

Expected:

- PASS

**Step 3: Commit**

```bash
git add src/perp_platform/control_plane/queries.py src/perp_platform/control_plane/app.py src/perp_platform/control_plane/__init__.py tests/perp_platform/control_plane/test_audit_query.py
git commit -m "fix: harden audit query redaction and time filters"
```

### Task 3: Update docs and run full verification

**Files:**
- Modify: `README.md`
- Modify: `docs/architecture/AUDIT_LOG.md`
- Modify: `docs/plans/2026-03-21-issue-162-audit-query-hardening-design.md`
- Modify: `docs/plans/2026-03-21-issue-162-audit-query-hardening.md`

**Step 1: Update docs**

- 明确 shared audit view 默认 redacted
- 明确时间窗口使用 RFC3339 语义

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
git add README.md docs/architecture/AUDIT_LOG.md docs/plans/2026-03-21-issue-162-audit-query-hardening-design.md docs/plans/2026-03-21-issue-162-audit-query-hardening.md
git commit -m "docs: add audit query hardening notes"
```
