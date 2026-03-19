# 主 Agent 第二阶段设计：GH Sync 与 Start

## 目标

在现有 issue orchestrator bootstrap 基础上，补齐主 agent 的两个关键入口能力：

- 直接从 GitHub 同步 child issue 状态，不再依赖手写 `issues.json`
- 用单条 `start` 命令把主 agent 推进到“可派发 subagent”的状态

本阶段仍保持“主 agent 编排、subagent 执行”的边界，不在仓库脚本里直接自动派发 subagent。

## 非目标

- 不实现长驻循环 runner
- 不在脚本里直接调用 `spawn_agent`
- 不自动 merge、close GitHub issue
- 不自动创建真实 worktree
- 不在本阶段实现多 issue 并行开发

## 现状

当前已有能力：

- `approval create/show/check`
- `next`
- `claim`
- `prepare`
- `accept`
- `block`
- `close`

现有缺口：

- `next/claim/prepare` 仍依赖手工维护 `issues.json`
- `prepare` 只输出最小 payload，还不是完整的 dispatch pack
- 缺少一个聚合入口把授权检查、同步、选 issue、认领和准备串起来

## 推荐方案

采用三段式增量架构：

1. `gh sync`  
从 GitHub 读取 issue 元数据，规范化写入本地快照。

2. 本地调度层  
继续用本地快照与 runtime state 进行顺序判定、认领和授权检查。

3. `dispatch pack`  
在 `prepare` 和 `start` 输出中生成结构化任务包和渲染好的 `subagent_prompt`。

选择这个方案的原因：

- 保留当前可测的本地调度层，不把顺序判定直接绑死在 `gh` 网络调用上
- 让 GitHub 读取和本地顺序规则解耦，便于测试和恢复
- 主 agent 可以用一条命令进入可派发状态，但仍保留人工审阅与控制点

## 数据源与真相边界

顺序控制继续使用双源校验：

1. 结构真相源  
[ISSUE_HIERARCHY.md](D:/fqcex/docs/roadmap/ISSUE_HIERARCHY.md)

2. 运行真相源  
GitHub issue 元数据 + 本地 `approval_bundle` + 本地 `state.json`

GitHub 元数据负责：

- open / closed
- labels
- assignee
- body

`ISSUE_HIERARCHY.md` 负责：

- epic / tracking / child 顺序
- sibling 的固定先后

## `gh sync` 设计

新增命令：

```powershell
py scripts/issue_orchestrator.py gh sync
```

默认输出：

- `D:/fqcex/.codex/orchestrator/issues.json`

推荐实现方式：

- 用 `gh issue list` 读取 open 和 closed issue
- 对命中 `type/task`、`type/tracking`、`type/epic` 的 issue 做规范化
- 从 `ISSUE_HIERARCHY.md` 解析 child 顺序并补齐：
  - `tracking_issue_id`
  - `epic_issue_id`
  - `sequence_index`

推荐的 `issues.json` 条目结构：

```json
{
  "issue_id": 30,
  "issue_title": "统一模型：文档化真相字段与架构约束",
  "tracking_issue_id": 11,
  "epic_issue_id": 2,
  "sequence_index": 2,
  "state": "open",
  "type_label": "type/task",
  "phase_labels": ["phase/1"],
  "area_labels": ["area/architecture"],
  "assignees": ["dao1oad"],
  "body": "...",
  "body_links": {
    "tracking_parent": 11,
    "epic": 2
  }
}
```

## “唯一 next ready issue” 判定

一个 child issue 只有同时满足下面条件时才是 `ready`：

- 在 `ISSUE_HIERARCHY.md` 中属于 `type/task`
- `state = open`
- 所有前序 sibling 已关闭
- 未被其他活跃 orchestrator state 占用
- assignee 为空或为当前主 agent 所属账号
- 在当前 `approval_bundle` 授权范围内

推荐输出分类：

- `ready`
- `blocked_by_order`
- `blocked_by_state`
- `blocked_by_assignee`
- `blocked_by_scope`
- `invalid_metadata`

这样 `next` 不只返回一个 issue，还能解释为什么其他 issue 当前不可执行。

## `dispatch pack` 设计

`prepare` 和 `start` 的输出应升级为三层结构：

1. `execution_context`
- issue / tracking / epic
- branch / worktree
- approval bundle
- model / reasoning effort

2. `constraints`
- allowed files
- forbidden files
- acceptance checks
- escalation triggers
- review requirements

3. `subagent_prompt`
- 一段可直接发给 `gpt-5.4` `xhigh` subagent 的渲染文本

推荐输出示例：

```json
{
  "branch": "codex/issue-30-model-docs-constraints",
  "worktree_path": "D:/fqcex/.worktrees/issue-30-model-docs-constraints",
  "execution_context": {
    "issue_id": 30,
    "issue_title": "统一模型：文档化真相字段与架构约束",
    "tracking_issue_id": 11,
    "epic_issue_id": 2,
    "approval_bundle_id": "exec-2026-03-19-001",
    "model": "gpt-5.4",
    "reasoning_effort": "xhigh"
  },
  "constraints": {
    "allowed_files": [],
    "forbidden_files": [],
    "acceptance_checks": [],
    "escalation_triggers": [
      "sibling_issue_required",
      "adr_or_runbook_change_required",
      "phase_boundary_conflict",
      "forbidden_file_change",
      "repeated_nonconverging_failures"
    ],
    "review_requirements": [
      "review evidence required",
      "verification required before merge"
    ]
  },
  "subagent_prompt": "..."
}
```

## `start` 设计

新增命令：

```powershell
py scripts/issue_orchestrator.py start
```

推荐行为：

1. 检查 `approval_bundle` 是否存在
2. 运行 `gh sync`
3. 运行 `next`
4. 运行 `claim`
5. 运行 `prepare`
6. 输出完整 dispatch pack

`start` 是主 agent 的聚合入口，但不是“一键自动开发”：

- 不自动派发 subagent
- 不自动建真实 worktree
- 不自动 merge / close

它的目标是把主 agent 推到“可派发状态”。

## 命令设计

推荐新增或扩展以下命令：

- `gh sync`
- `start`
- `prepare`：输出完整 dispatch pack

保留现有命令：

- `approval create/show/check`
- `next`
- `claim`
- `accept`
- `block`
- `close`

## 文件变更

建议修改：

- [issue_orchestrator.py](D:/fqcex/scripts/issue_orchestrator.py)
- [github_state.py](D:/fqcex/src/perp_platform/orchestrator/github_state.py)
- [dispatcher.py](D:/fqcex/src/perp_platform/orchestrator/dispatcher.py)
- [sequence.py](D:/fqcex/src/perp_platform/orchestrator/sequence.py)
- [models.py](D:/fqcex/src/perp_platform/orchestrator/models.py)
- [runtime_state.py](D:/fqcex/src/perp_platform/orchestrator/runtime_state.py)

可选新增：

- `D:/fqcex/src/perp_platform/orchestrator/gh_sync.py`

新增测试：

- `D:/fqcex/tests/orchestrator/test_gh_sync.py`
- `D:/fqcex/tests/orchestrator/test_cli_start.py`

## 测试策略

按 TDD 增量实现：

1. `gh sync` 规范化测试
2. `start` 聚合流程测试
3. `prepare` 扩展输出测试
4. 顺序判定的 assignee / scope / metadata 边界测试

## 验收标准

完成后应满足：

- 不再需要手工维护 `issues.json`
- `gh sync` 能把 GitHub issue 状态规范化为本地快照
- `start` 能用一条命令进入可派发状态
- `prepare` 输出完整 dispatch pack
- dispatch pack 可直接交给 `gpt-5.4` `xhigh` subagent
- 顺序、授权、单 writer 约束仍成立
- 仓库全量测试继续通过
