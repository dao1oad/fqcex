# fqcex 项目记忆系统设计

## 背景

`fqcex` 当前已经建立了治理文档、roadmap、ADR、runbook 和 GitHub issue / milestone 结构，但还缺少一套能让**新开的会话快速掌握项目当前代码现状、活跃分支、最近进展和下一步切入点**的记忆系统。

项目现状的痛点主要有三类：

1. 稳定事实分散在 `README`、`AGENTS.md`、`docs/architecture`、`docs/roadmap` 中。
2. 当前进展分散在 Git 分支、worktree、最近提交、open issues 和未合并工作里。
3. 新会话缺少统一入口，不知道先看哪些文件、先跑哪些命令。

## 目标

建立一套“**稳定记忆 + 自动快照**”的项目记忆系统，让任何新会话都能在较短时间内回答下面这些问题：

- 当前项目做什么、范围冻结到哪里？
- 现在代码主线做到了哪一步？
- 有哪些活跃 worktree / feature branch？
- 最近的关键提交和未合并工作是什么？
- 当前 GitHub issue / PR / milestone 进度如何？
- 新会话第一步应该看什么、跑什么？

## 非目标

- 不构建数据库或外部持久化服务。
- 不引入复杂向量索引或语义检索。
- 不把所有历史对话原样存仓库。
- 不在第一阶段自动调用大模型总结仓库内容。

## 方案对比

### 方案 A：单文件记忆

只维护一个 `docs/memory.md`。

优点：

- 结构简单
- 成本最低

缺点：

- 很快失真
- 无法体现 worktree、分支、issue、最近提交等动态状态
- 只能作为人工摘要，不能作为真实代码现状快照

### 方案 B：多份记忆文档，全部手工维护

例如：

- `PROJECT_STATE.md`
- `ACTIVE_WORK.md`
- `SESSION_HANDOFF.md`

优点：

- 信息分层清楚
- 便于人工阅读

缺点：

- 更新成本高
- 很容易与 GitHub / Git 真实状态脱节

### 方案 C：分层记忆文档 + 自动快照脚本

这是推荐方案。

做法：

- 用手工文档记录稳定事实、长期边界、当前切入指引
- 用脚本从 Git / GitHub 读取动态状态，自动生成快照文档

优点：

- 同时解决“长期记忆”和“当前状态”
- 新会话有统一入口
- 不需要引入额外外部系统

缺点：

- 需要补脚本和文档模板
- GitHub CLI 未登录时，GitHub 部分信息需要降级处理

## 选型结论

采用 **方案 C：分层记忆文档 + 自动快照脚本**。

## 总体结构

```txt
docs/
  memory/
    PROJECT_STATE.md
    ACTIVE_WORK.md
    SESSION_HANDOFF.md
    generated/
      project_snapshot.md
scripts/
  update_project_memory.py
  project_context.ps1
```

## 组件设计

### 1. `PROJECT_STATE.md`

作用：记录**稳定事实**。

内容包括：

- 项目目标
- 当前阶段范围冻结
- 主架构结论
- 当前主线能力
- 已完成的重大基础设施
- 当前不做的事情

更新规则：

- 只在架构、范围、主线能力发生明确变化时更新
- 不记录临时试验或短期状态

### 2. `ACTIVE_WORK.md`

作用：记录**当前进行中的重要工作**。

内容包括：

- 活跃分支
- 未合并的关键 feature work
- 当前进行中的 epic / issues
- 已知阻塞
- 下一批推荐优先项

更新规则：

- 每次关键 feature 开始、完成、切换优先级时更新
- 可以引用自动快照，但保留人工解释

### 3. `SESSION_HANDOFF.md`

作用：作为**新会话入口**。

内容包括：

- 新会话先读哪些文件
- 先执行哪些脚本/命令
- 当前最推荐的工作切入点
- 当前需要注意的风险或未合并分支

更新规则：

- 当“新会话最佳入口”发生变化时更新

### 4. `generated/project_snapshot.md`

作用：记录**自动生成的当前项目快照**。

来源：

- `git status --branch`
- `git branch --all`
- `git worktree list`
- `git log --oneline`
- `gh issue list`
- `gh pr list`
- 关键文档/目录存在性检查

约束：

- 自动生成，不手工编辑
- 每次运行脚本覆盖更新

## 自动脚本设计

### `scripts/update_project_memory.py`

职责：

- 读取仓库当前状态
- 尝试读取 GitHub 当前 issue / PR 状态
- 生成 `docs/memory/generated/project_snapshot.md`

脚本输出应至少包含：

1. 生成时间
2. 仓库根路径
3. 当前分支与 `git status`
4. 当前 worktree 列表
5. 最近提交
6. 本地分支列表
7. 远端分支摘要
8. open issues 摘要
9. open PR 摘要
10. 关键文档存在性
11. 当前推荐入口文件列表

降级行为：

- 若 `gh` 不可用或未登录，则保留 Git 部分并在快照中注明 GitHub 数据不可用

### `scripts/project_context.ps1`

职责：

- 给新会话提供一条本地命令入口
- 直接在终端打印高价值上下文

输出应尽量精简，优先显示：

- 当前分支
- worktree
- 最近提交
- `docs/memory` 关键文件路径
- 自动快照路径

## 新会话工作流

建议在 `AGENTS.md` 中明确：

1. 先看 `docs/memory/PROJECT_STATE.md`
2. 再看 `docs/memory/ACTIVE_WORK.md`
3. 然后运行 `python scripts/update_project_memory.py`
4. 再看 `docs/memory/generated/project_snapshot.md`
5. 最后根据 `SESSION_HANDOFF.md` 选择切入点

## 错误处理

### GitHub CLI 不可用

- 不中断脚本
- 在快照中标记：`GitHub metadata unavailable`

### 当前目录不在 Git 仓库

- 脚本明确报错并退出

### `docs/memory/generated` 不存在

- 脚本自动创建目录

## 测试策略

### Python 单元测试

覆盖：

- Markdown 输出结构
- GitHub 不可用时的降级逻辑
- 快照文件生成逻辑

### PowerShell 脚本验证

覆盖：

- 能在仓库根路径成功输出上下文
- 失败时给出明确错误

## 验收标准

1. 仓库内存在 `docs/memory` 三个手工维护文件。
2. 存在 `scripts/update_project_memory.py` 和 `scripts/project_context.ps1`。
3. 运行 Python 脚本后会生成 `docs/memory/generated/project_snapshot.md`。
4. 新会话按文档入口可快速看到项目范围、当前进展、活跃分支与 issue / PR 摘要。
5. `AGENTS.md` 和 `README.md` 会明确引用这套记忆系统入口。
