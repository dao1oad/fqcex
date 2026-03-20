# Issue 59 WebSocket Disconnect Injector Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 增加一个可输出标准化断连注入计划的 WebSocket disconnect injector 脚本。

**Architecture:** 使用单文件 CLI 脚本接收 venue / stream / duration 等输入，输出 JSON 注入计划到 stdout 或文件。测试通过子进程调用脚本校验返回码和 JSON 内容。

**Tech Stack:** Python 3.12, argparse, json, pytest

---

### Task 1: Add failing injector tests

**Files:**
- Create: `tests/ops/test_ws_disconnect_injector.py`

**Step 1: Write the failing test**

覆盖 stdout 输出和非法 duration。

**Step 2: Run test to verify it fails**

Run: `py -m pytest tests/ops/test_ws_disconnect_injector.py -q`

Expected: FAIL because `scripts/inject_ws_disconnect.py` does not exist yet.

### Task 2: Implement CLI injector

**Files:**
- Create: `scripts/inject_ws_disconnect.py`
- Test: `tests/ops/test_ws_disconnect_injector.py`

**Step 1: Write minimal implementation**

实现参数解析、duration 校验、JSON 输出和可选文件写入。

**Step 2: Run test to verify it passes**

Run: `py -m pytest tests/ops/test_ws_disconnect_injector.py -q`

Expected: PASS

### Task 3: Verify end to end

**Files:**
- Modify: `docs/plans/2026-03-20-issue-59-ws-disconnect-design.md`
- Modify: `docs/plans/2026-03-20-issue-59-ws-disconnect.md`

**Step 1: Run targeted tests**

Run: `py -m pytest tests/ops/test_ws_disconnect_injector.py -q`

Expected: PASS

**Step 2: Run full test suite**

Run: `py -m pytest tests -q`

Expected: PASS

**Step 3: Final commit**

```bash
git add scripts/inject_ws_disconnect.py tests/ops/test_ws_disconnect_injector.py docs/plans/2026-03-20-issue-59-ws-disconnect-design.md docs/plans/2026-03-20-issue-59-ws-disconnect.md
git commit -m "feat: add websocket disconnect injector"
```
