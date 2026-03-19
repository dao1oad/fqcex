# #26 Config Bootstrap Contract Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 为 `perp_platform` 建立最小配置初始化契约，让入口点能基于合法配置对象完成启动。

**Architecture:** 通过标准库 `dataclass` 定义 `AppConfig`，并以环境变量作为唯一配置来源。`cli.main()` 只做一层薄集成：加载配置并输出稳定启动文案，不引入 runtime 细节。

**Tech Stack:** Python 3.12, `pytest`, `dataclasses`, `typing`, `os`.

---

### Task 1: 建立配置契约测试

**Files:**
- Create: `tests/perp_platform/test_config.py`
- Modify: `tests/perp_platform/test_entrypoint.py`

**Step 1: Write the failing test**

```python
from perp_platform.config import AppConfig, load_config


def test_load_config_returns_defaults():
    config = load_config({})
    assert config == AppConfig(
        app_name="perp-platform",
        environment="dev",
        log_level="INFO",
    )
```

**Step 2: Run test to verify it fails**

Run: `py -m pytest tests/perp_platform/test_config.py -q`
Expected: FAIL because `perp_platform.config` does not exist yet.

**Step 3: Commit**

```bash
git add tests/perp_platform/test_config.py tests/perp_platform/test_entrypoint.py
git commit -m "test: add config bootstrap contract"
```

### Task 2: 实现配置对象与加载逻辑

**Files:**
- Create: `src/perp_platform/config.py`
- Modify: `src/perp_platform/cli.py`
- Modify: `src/perp_platform/__init__.py`
- Modify: `tests/perp_platform/test_config.py`
- Modify: `tests/perp_platform/test_entrypoint.py`

**Step 1: Write minimal implementation**

```python
@dataclass(frozen=True)
class AppConfig:
    app_name: str
    environment: str
    log_level: str


def load_config(environ: Mapping[str, str] | None = None) -> AppConfig:
    ...
```

**Step 2: Run targeted tests**

Run: `py -m pytest tests/perp_platform/test_config.py tests/perp_platform/test_entrypoint.py -q`
Expected: PASS

**Step 3: Run full tests**

Run: `py -m pytest tests -q`
Expected: PASS

**Step 4: Commit**

```bash
git add src/perp_platform tests/perp_platform
git commit -m "feat: add config bootstrap contract"
```

### Task 3: 更新文档并准备 PR

**Files:**
- Create: `docs/plans/2026-03-19-issue-26-config-bootstrap-contract-design.md`
- Create: `docs/plans/2026-03-19-issue-26-config-bootstrap-contract.md`

**Step 1: Verify issue boundary**

Run: `git status --short`
Expected: 仅包含配置契约、CLI 薄集成、测试和计划文档，不包含共享测试基座。

**Step 2: Capture verification**

Run: `py -m pytest tests/perp_platform/test_config.py tests/perp_platform/test_entrypoint.py -q`
Expected: PASS

**Step 3: Commit**

```bash
git add docs/plans/2026-03-19-issue-26-config-bootstrap-contract-design.md docs/plans/2026-03-19-issue-26-config-bootstrap-contract.md
git commit -m "docs: add issue 26 design and plan"
```
