# Issue 145 Control Plane Skeleton Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 为 control-plane 增加最小可运行的 HTTP skeleton，提供统一 envelope、`health` 和 `readiness` 端点。

**Architecture:** 使用 Python 标准库 `http.server` 实现薄 HTTP 层，在 `app.py` 中保留纯函数式 dispatch 与 envelope 生成逻辑。先只支持 `GET /control-plane/v1/health` 与 `GET /control-plane/v1/readiness`。

**Tech Stack:** Python 3.12, `http.server`, `json`, `urllib.request`, `pytest`

---

### Task 1: Add failing control-plane skeleton tests

**Files:**
- Create: `tests/perp_platform/control_plane/test_http_skeleton.py`
- Test: `tests/perp_platform/control_plane/test_http_skeleton.py`

**Step 1: Write the failing test**

- 定义：
  - `health` success envelope
  - `readiness` success envelope
  - unknown path error envelope
  - real server smoke test

**Step 2: Run test to verify it fails**

Run: `py -m pytest tests/perp_platform/control_plane/test_http_skeleton.py -q`

Expected:

- FAIL，因为 `perp_platform.control_plane` 尚不存在

**Step 3: Commit**

```bash
git add tests/perp_platform/control_plane/test_http_skeleton.py
git commit -m "test: define control plane skeleton contract"
```

### Task 2: Implement minimal control-plane package

**Files:**
- Create: `src/perp_platform/control_plane/__init__.py`
- Create: `src/perp_platform/control_plane/app.py`
- Create: `src/perp_platform/control_plane/server.py`
- Create: `src/perp_platform/control_plane/__main__.py`
- Test: `tests/perp_platform/control_plane/test_http_skeleton.py`

**Step 1: Write minimal implementation**

- `ControlPlaneApp.handle(method, path)`
- success / error envelope helpers
- `serve_control_plane(host, port)`
- `python -m perp_platform.control_plane`

**Step 2: Run targeted tests**

Run: `py -m pytest tests/perp_platform/control_plane/test_http_skeleton.py -q`

Expected:

- PASS

**Step 3: Commit**

```bash
git add src/perp_platform/control_plane/__init__.py src/perp_platform/control_plane/app.py src/perp_platform/control_plane/server.py src/perp_platform/control_plane/__main__.py tests/perp_platform/control_plane/test_http_skeleton.py
git commit -m "feat: add control plane http skeleton"
```

### Task 3: Update docs and verify full suite

**Files:**
- Modify: `README.md`
- Modify: `docs/plans/2026-03-21-issue-145-control-plane-skeleton-design.md`
- Modify: `docs/plans/2026-03-21-issue-145-control-plane-skeleton.md`

**Step 1: Update docs**

- 在 `README.md` 中补充最小 control-plane 启动方式

**Step 2: Run verification**

Run:

```bash
py -m pytest tests/perp_platform/control_plane/test_http_skeleton.py -q
py -m pytest tests -q
```

Expected:

- PASS

**Step 3: Commit**

```bash
git add README.md docs/plans/2026-03-21-issue-145-control-plane-skeleton-design.md docs/plans/2026-03-21-issue-145-control-plane-skeleton.md
git commit -m "docs: add issue 145 control plane plan"
```
