# Issue 80 Worktree Memory Contract Design

## Goal

修正 `project_snapshot` 在新建 worktree 下运行时的测试假设，使断言不再依赖已经删除的历史分支名。

## Scope

- 修改 `tests/memory/test_update_project_memory.py`
- 保持 `scripts/update_project_memory.py` 输出结构不变
- 不扩展新的快照字段

## Recommendation

把硬编码的历史分支名断言收口为对当前稳定主线分支 `main` 的检查，并保留对 `Local Branches`、`Remote Branches`、仓库根路径和工作区状态的现有验证。
