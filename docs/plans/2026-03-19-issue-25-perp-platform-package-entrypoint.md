# #25 Perp Platform Package Entrypoint Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 为 `perp_platform` 建立最小 Python 包与统一入口点，使后续配置契约和测试基座有稳定挂点。

**Architecture:** 在仓库根级引入标准 `src` 布局和最小 `pyproject.toml`。入口统一收敛到 `perp_platform.cli.main()`，`python -m perp_platform` 复用同一执行路径，不引入配置或 runtime 细节。

**Tech Stack:** Python 3.12, `pytest`, standard library `argparse`, `pathlib`, package `src` layout.

---

### Task 1: 建立入口测试

**Files:**
- Create: `tests/perp_platform/test_entrypoint.py`
- Reference: `tests/memory/test_memory_docs.py`

**Step 1: Write the failing test**

```python
from __future__ import annotations

import subprocess
import sys

from perp_platform.cli import main


def test_main_returns_zero_and_prints_bootstrap_message(capsys):
    exit_code = main([])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "perp-platform bootstrap ready" in captured.out


def test_module_entrypoint_runs_successfully():
    result = subprocess.run(
        [sys.executable, "-m", "perp_platform"],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert "perp-platform bootstrap ready" in result.stdout
```

**Step 2: Run test to verify it fails**

Run: `py -m pytest tests/perp_platform/test_entrypoint.py -q`
Expected: FAIL because `perp_platform` package does not exist yet.

**Step 3: Commit**

```bash
git add tests/perp_platform/test_entrypoint.py
git commit -m "test: add entrypoint contract for perp-platform"
```

### Task 2: 实现最小包与入口

**Files:**
- Create: `pyproject.toml`
- Create: `src/perp_platform/__init__.py`
- Create: `src/perp_platform/__main__.py`
- Create: `src/perp_platform/cli.py`
- Modify: `tests/perp_platform/test_entrypoint.py`

**Step 1: Write minimal implementation**

```python
def main(argv: list[str] | None = None) -> int:
    print("perp-platform bootstrap ready")
    return 0
```

```python
from .cli import main

raise SystemExit(main())
```

**Step 2: Run test to verify it passes**

Run: `py -m pytest tests/perp_platform/test_entrypoint.py -q`
Expected: PASS

**Step 3: Run full tests**

Run: `py -m pytest tests -q`
Expected: PASS with no regressions.

**Step 4: Commit**

```bash
git add pyproject.toml src/perp_platform tests/perp_platform/test_entrypoint.py
git commit -m "feat: add perp-platform package entrypoint"
```

### Task 3: 更新文档并准备 PR

**Files:**
- Create: `docs/plans/2026-03-19-issue-25-perp-platform-package-entrypoint-design.md`
- Create: `docs/plans/2026-03-19-issue-25-perp-platform-package-entrypoint.md`

**Step 1: Verify issue boundary**

Run: `git diff --stat`
Expected: 仅包含 `#25` 需要的包、入口、测试和计划文档，不包含配置系统或共享测试基座。

**Step 2: Capture verification**

Run: `py -m perp_platform`
Expected: 输出 `perp-platform bootstrap ready`

**Step 3: Commit**

```bash
git add docs/plans/2026-03-19-issue-25-perp-platform-package-entrypoint-design.md docs/plans/2026-03-19-issue-25-perp-platform-package-entrypoint.md
git commit -m "docs: add issue 25 design and implementation plan"
```
