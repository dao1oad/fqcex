# Issue 80 Worktree Memory Contract Implementation Plan

## Goal

让 `tests/memory/test_update_project_memory.py` 在 worktree 场景下稳定通过，而不绑定旧分支名。

## Steps

1. 保留现有失败用例，确认它因为 `codex/ci-cd-bootstrap` 的历史断言而失败。
2. 仅修改该断言，改为检查当前快照包含 `main`。
3. 运行：
   - `py -m pytest tests/memory/test_update_project_memory.py -q`
   - `py -m pytest tests -q`
