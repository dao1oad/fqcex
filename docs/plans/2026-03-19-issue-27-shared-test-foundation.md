# #27 Shared Test Foundation Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 为 `perp_platform` 建立最小共享测试基座，消除当前测试中的路径注入、环境清理和 CLI 调用重复。

**Architecture:** 通过 `tests/conftest.py` 提供基础环境隔离，在 `tests/perp_platform/support/` 中集中实现配置和 CLI 测试 helper。helper 只包装当前真实契约，不引入业务专用 fixture。

**Tech Stack:** Python 3.12, `pytest`, `dataclasses`, `contextlib`, `io`, `importlib`, `sys`.

---

### Task 1: 建立 support contract 测试

**Files:**
- Create: `tests/perp_platform/test_support_contract.py`
- Modify: `tests/perp_platform/test_config.py`
- Modify: `tests/perp_platform/test_entrypoint.py`

**Step 1: Write the failing test**

```python
from tests.perp_platform.support.cli import run_cli
from tests.perp_platform.support.config import make_test_config


def test_make_test_config_returns_app_config():
    config = make_test_config(environment="test")
    assert config.environment == "test"
```

**Step 2: Run test to verify it fails**

Run: `py -m pytest tests/perp_platform/test_support_contract.py -q`
Expected: FAIL because support package does not exist yet.

**Step 3: Commit**

```bash
git add tests/perp_platform/test_support_contract.py tests/perp_platform/test_config.py tests/perp_platform/test_entrypoint.py
git commit -m "test: add shared test support contract"
```

### Task 2: 实现共享测试 helper

**Files:**
- Create: `tests/conftest.py`
- Create: `tests/perp_platform/support/__init__.py`
- Create: `tests/perp_platform/support/config.py`
- Create: `tests/perp_platform/support/cli.py`
- Modify: `tests/perp_platform/test_support_contract.py`
- Modify: `tests/perp_platform/test_config.py`
- Modify: `tests/perp_platform/test_entrypoint.py`

**Step 1: Write minimal implementation**

```python
def make_test_config(...):
    return AppConfig(...)


def run_cli(...):
    return CLIResult(exit_code=..., stdout=...)
```

**Step 2: Run targeted tests**

Run: `py -m pytest tests/perp_platform/test_support_contract.py tests/perp_platform/test_config.py tests/perp_platform/test_entrypoint.py -q`
Expected: PASS

**Step 3: Run full tests**

Run: `py -m pytest tests -q`
Expected: PASS

**Step 4: Commit**

```bash
git add tests/conftest.py tests/perp_platform
git commit -m "test: add shared perp-platform test foundation"
```

### Task 3: 更新文档并准备 PR

**Files:**
- Create: `docs/plans/2026-03-19-issue-27-shared-test-foundation-design.md`
- Create: `docs/plans/2026-03-19-issue-27-shared-test-foundation.md`

**Step 1: Verify issue boundary**

Run: `git status --short`
Expected: 仅包含测试 support 层、测试迁移和计划文档，不包含业务逻辑扩展。

**Step 2: Capture verification**

Run: `py -m pytest tests/perp_platform -q`
Expected: PASS

**Step 3: Commit**

```bash
git add docs/plans/2026-03-19-issue-27-shared-test-foundation-design.md docs/plans/2026-03-19-issue-27-shared-test-foundation.md
git commit -m "docs: add issue 27 design and plan"
```
