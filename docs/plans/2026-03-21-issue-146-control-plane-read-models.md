# Issue 146 Control Plane Read Models Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 为 control-plane 增加 venue / instrument / recovery / checker 四类只读查询接口。

**Architecture:** 先在 `queries.py` 中定义 read model dataclasses 与 query backend protocol，再在 `app.py` 中扩展 GET handlers。第一版使用 `InMemoryControlPlaneQueryBackend` 作为测试和合同入口，不直接连接数据库。

**Tech Stack:** Python 3.12, `dataclasses`, `typing.Protocol`, `http.server`, `pytest`

---

### Task 1: Add failing read-model query tests

**Files:**
- Create: `tests/perp_platform/control_plane/test_read_models.py`
- Test: `tests/perp_platform/control_plane/test_read_models.py`

**Step 1: Write the failing test**

- 覆盖：
  - venues list / detail
  - instruments list / detail
  - recovery runs list / detail
  - checker signals list / detail
  - missing resource -> `404`

**Step 2: Run test to verify it fails**

Run: `py -m pytest tests/perp_platform/control_plane/test_read_models.py -q`

Expected:

- FAIL，因为 `queries.py` 和对应 handlers 尚不存在

**Step 3: Commit**

```bash
git add tests/perp_platform/control_plane/test_read_models.py
git commit -m "test: define control plane read model queries"
```

### Task 2: Implement query models and handlers

**Files:**
- Create: `src/perp_platform/control_plane/queries.py`
- Modify: `src/perp_platform/control_plane/app.py`
- Modify: `src/perp_platform/control_plane/__init__.py`
- Test: `tests/perp_platform/control_plane/test_read_models.py`
- Test: `tests/perp_platform/control_plane/test_http_skeleton.py`

**Step 1: Add minimal implementation**

- 定义四类 view dataclasses
- 定义 `ControlPlaneQueryBackend`
- 定义 `InMemoryControlPlaneQueryBackend`
- 在 `app.py` 中扩展 GET resource routing

**Step 2: Run targeted tests**

Run:

```bash
py -m pytest tests/perp_platform/control_plane/test_read_models.py -q
py -m pytest tests/perp_platform/control_plane/test_http_skeleton.py -q
```

Expected:

- PASS

**Step 3: Commit**

```bash
git add src/perp_platform/control_plane/queries.py src/perp_platform/control_plane/app.py src/perp_platform/control_plane/__init__.py tests/perp_platform/control_plane/test_read_models.py
git commit -m "feat: add control plane read model queries"
```

### Task 3: Update docs and run full verification

**Files:**
- Modify: `README.md`
- Modify: `docs/plans/2026-03-21-issue-146-control-plane-read-models-design.md`
- Modify: `docs/plans/2026-03-21-issue-146-control-plane-read-models.md`

**Step 1: Update README**

- 补充当前可用 query 端点

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
git add README.md docs/plans/2026-03-21-issue-146-control-plane-read-models-design.md docs/plans/2026-03-21-issue-146-control-plane-read-models.md
git commit -m "docs: add issue 146 read model plan"
```
