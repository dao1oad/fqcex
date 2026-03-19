# 主 Agent Issue 编排设计

## 目标

在仓库内建立一个可重复执行的 issue 编排机制，由主 agent 负责：

- 按 `ISSUE_HIERARCHY.md` 选出唯一正确的下一个 child issue
- 认领、分发、验收并关闭 issue
- 只在安全位置启用必要并发
- 强制所有 subagent 使用 `gpt-5.4` 和 `xhigh`

本设计同时覆盖运行规范和仓库内调度器，不把顺序控制只留在提示词里。

## 非目标

- 不在第一版实现多 issue 并行开发
- 不让 subagent 直接 merge、close issue 或更新 tracking
- 不绕过 `AGENTS.md` 与 `ISSUE_HIERARCHY.md`
- 不把 GitHub 平台规则写成调度器内部的硬编码分支保护替代品

## 约束与原则

- issue 顺序以 [ISSUE_HIERARCHY.md](D:/fqcex/docs/roadmap/ISSUE_HIERARCHY.md) 为结构真相源
- issue 运行状态以 GitHub issue 状态、assignee 和本地 runtime state 为运行真相源
- 只允许从 `type/task` issue 直接进入实现
- 同一时刻只允许一个 issue 处于 `IMPLEMENTING`
- 同一 issue 只允许一个写入型 subagent
- 只读 sidecar subagent 只做探索、验证、预审，不得改代码

## 总体架构

系统由四个角色组成：

1. 主 agent  
主控顺序、认领 issue、生成计划、派发 subagent、做最终验收、合并并关闭 issue。

2. owner subagent  
只处理一个 child issue，在指定 worktree 内完成最小闭环实现。owner 必须是唯一 writer。

3. sidecar subagent  
只读辅助 agent，用于并发探索、验证和预审。sidecar 不得编辑文件或提交结果。

4. 仓库内调度器  
以脚本和 Python 模块实现顺序判定、状态持久化、派发输入生成和验收前检查。

## 顺序控制模型

主 agent 的 issue 选择规则固定为：

1. 只考虑 open 且属于 `type/task` 的 child issue
2. 只考虑其前序 sibling 已全部关闭的 issue
3. 默认不跨 tracking parent 跳过未完成 issue
4. 若下一个 child issue 因边界不清、依赖未满足或治理冲突而不可执行，状态标记为 `BLOCKED`，而不是自动跳到后续 issue

第一版不支持基于“看起来独立”就并发推进多个 child issue。

## 必要并发模型

必要并发限定为“串行推进 issue，受控并发 issue 内部任务”。

允许并发的阶段只有三个：

1. `CONTEXT_GATHERING`  
主 agent 可同时派两个只读 sidecar：
   - explorer A：读取代码和依赖边界
   - explorer B：读取 issue、文档、测试约束

2. `VERIFYING`  
owner 完成实现后，主 agent 可同时派：
   - verifier：执行验证命令
   - reviewer：执行只读预审

3. `NEXT_ISSUE_PREFETCH`  
当前 issue 已进入 `VERIFYING` 或 `REVIEWING` 时，可对下一个 issue 做只读上下文预取，但不得建分支、写计划或改代码。

禁止并发的场景：

- 两个 writer 同时修改同一 issue
- 两个 child issue 同时进入 `IMPLEMENTING`
- 当前 issue 未关闭就让后续 issue 开始编码
- 基于旧 `head SHA` 的验证结果被继续沿用

## 状态机

推荐状态机如下：

- `READY`
- `CLAIMED`
- `CONTEXT_GATHERING`
- `DESIGNING`
- `PLAN_READY`
- `DISPATCHED`
- `IMPLEMENTING`
- `VERIFYING`
- `REVIEW_FIXING`
- `ACCEPTED`
- `MERGED`
- `CLOSED`
- `BLOCKED`

状态规则：

- 只有 `IMPLEMENTING` 允许 writer 改代码
- `VERIFYING` 期间 owner 不得继续修改代码
- 只要 `head SHA` 改变，旧的 verifier / reviewer 结果立即失效
- 进入 `BLOCKED` 后，主 agent 停止推进后续实现，只输出阻塞原因与建议动作

## 派发协议

主 agent 派发给 subagent 的上下文必须结构化，至少包含：

- `issue_id`
- `issue_title`
- `base_branch`
- `worktree_path`
- `ownership_scope`
- `allowed_files`
- `forbidden_files`
- `acceptance_checks`
- `model = gpt-5.4`
- `reasoning_effort = xhigh`

owner subagent 的硬约束：

- 一次只处理一个 child issue
- 只能在指定 worktree 工作
- 只能编辑 `allowed_files`
- 不得关闭 issue、合并分支或更新 tracking
- 必须返回修改摘要、修改文件、运行命令、验证结果、风险和 blocker

sidecar subagent 的硬约束：

- 不得编辑文件
- 不得创建提交
- 输出必须绑定当前 `base SHA` 和 `head SHA`
- 只能返回结论和证据

## 主 Agent 验收

主 agent 不能直接信任 subagent 输出，必须做 acceptance。

acceptance 分为五步：

1. 边界检查  
确认改动只落在本 issue 的负责范围内。

2. 顺序检查  
确认没有提前实现后续 issue 的内容。

3. 验证检查  
确认验证命令已在当前 `head SHA` 上运行并通过。

4. review 检查  
确认已有独立 review evidence，且与当前 diff 匹配。

5. 交付检查  
确认 issue、tracking、文档和治理动作已完成。

任一步失败时：

- 小问题：回到 `REVIEW_FIXING`
- 越界或顺序错误：直接拒收，并要求拆新 sibling issue 或进入 `BLOCKED`

## 失败重试与升级

失败分为三类：

1. 可重试失败  
例如网络安装失败、GitHub API 暂时失败、测试抖动。  
策略：自动重试最多 2 次。

2. 可修复失败  
例如测试失败、review findings、实现越界。  
策略：退回同一个 owner subagent 修复。

3. 阻塞失败  
例如前置 issue 未完成、issue 边界不清、与 Phase 1 冻结边界冲突。  
策略：进入 `BLOCKED`，停止后续推进，输出建议动作。

建议阈值：

- 自动重试上限：2
- 同一 issue 修复循环上限：3

超过阈值后升级为 `BLOCKED`。

## 仓库内文件布局

第一版建议实现以下文件：

- [scripts/issue_orchestrator.py](D:/fqcex/scripts/issue_orchestrator.py)
- [models.py](D:/fqcex/src/perp_platform/orchestrator/models.py)
- [sequence.py](D:/fqcex/src/perp_platform/orchestrator/sequence.py)
- [github_state.py](D:/fqcex/src/perp_platform/orchestrator/github_state.py)
- [runtime_state.py](D:/fqcex/src/perp_platform/orchestrator/runtime_state.py)
- [dispatcher.py](D:/fqcex/src/perp_platform/orchestrator/dispatcher.py)
- [test_sequence.py](D:/fqcex/tests/orchestrator/test_sequence.py)
- [test_runtime_state.py](D:/fqcex/tests/orchestrator/test_runtime_state.py)
- [issue-orchestrator.md](D:/fqcex/docs/runbooks/issue-orchestrator.md)

本地 runtime state 记录在：

- `D:/fqcex/.codex/orchestrator/state.json`

该文件不进入 git，只保存运行账本：

- 当前 active issue
- 当前状态
- active worktree
- active branch
- owner / sidecar agent id
- `base SHA`
- `head SHA`
- 重试次数
- blocker 原因

## CLI 设计

第一版 CLI 建议支持：

- `next`：输出下一个唯一 ready issue
- `claim <issue>`：认领 issue 并写入 runtime state
- `prepare <issue>`：生成 worktree、分支名、允许编辑边界和派发输入
- `status`：显示当前 orchestrator 状态
- `accept <issue>`：执行验收前结构检查
- `close <issue>`：完成 merge 后收尾
- `block <issue>`：记录阻塞原因与建议动作

第一版 CLI 不直接调用模型 API。它只负责可重复的顺序判定、状态记录和派发输入组装。

## Prompt / Policy 模板

主 agent prompt 必须固定：

- 你是 orchestrator master agent
- 只按 issue 顺序推进
- 不跳 issue
- 不同时实现多个 issue
- 你负责认领、分发、验收、合并、关闭
- acceptance 不得委托给 subagent

owner subagent prompt 必须固定：

- 只处理 issue `#X`
- 只在指定 worktree 工作
- 只编辑允许的文件
- 不得顺手修 unrelated 问题
- 不得关闭 issue 或合并

reviewer / verifier prompt 必须固定：

- 只读
- 不得编辑文件
- 结论必须绑定指定 SHA
- 必须显式报告越界或验证失败

## Approval Delegation Policy

方案确认权必须上收给主 agent，不得分散到各个 subagent。

规则如下：

- 用户只和主 agent 确认方案
- 主 agent 一旦拿到用户确认，就把“已批准推荐方案”冻结成派发输入
- subagent 可以做边界核对，但不得再次向用户发起方案确认
- subagent 默认按主 agent 冻结的推荐值直接执行
- 只有命中升级条件时，subagent 才能回到主 agent 请求新决策

主 agent 派发给 subagent 的 payload 中必须显式包含：

- `approved_design = true`
- `approval_owner = master_agent`
- `execution_mode = proceed_with_recommended_defaults`
- `recommended_defaults`
- `allowed_files`
- `forbidden_files`
- `escalation_triggers`

推荐的升级条件只有以下几类：

- 需要新 sibling issue 才能继续
- 会影响 `ADR`、`runbook` 或 `PHASE1_FREEZE`
- 必须修改 `forbidden_files`
- 推荐方案的前提被仓库现状否定
- 连续修复超过阈值仍不收敛

这条策略的目的，是避免每个 subagent 都在 superpowers 流程里重复执行“向用户确认方案”，从而把确认集中到主 agent，把执行留给 subagent。

## Execution Approval Template

为避免后续自动执行过程中不断停下来确认，主 agent 应在开始前一次性向用户发起“执行授权包”确认。推荐模板如下：

### 1. 执行范围

- 要连续推进的 issue 范围
- 是否严格按 [ISSUE_HIERARCHY.md](D:/fqcex/docs/roadmap/ISSUE_HIERARCHY.md) 顺序执行
- 是否允许跳过 blocked issue

推荐默认值：

- 明确 issue 范围，例如 `#30 -> #33`
- 严格按 issue 顺序执行
- 不允许自动跳过 blocked issue

### 2. 默认决策规则

- 未被用户单独点名的实现分歧，是否统一采用主 agent 推荐值
- subagent 是否允许按推荐值直接执行，不再二次确认

推荐默认值：

- `execution_mode = proceed_with_recommended_defaults`
- 所有普通实现分歧默认采用主 agent 推荐值

### 3. 并发规则

- 是否允许 issue 级别并发
- issue 内是否允许必要并发

推荐默认值：

- `issue_parallelism = 1`
- `write_agents_per_issue = 1`
- `read_only_sidecars_per_issue = 2`

### 4. 自动化权限

- 是否允许主 agent 自动认领 issue
- 是否允许自动创建 worktree / branch
- 是否允许自动派发 subagent
- 是否允许自动做 review 和 verification
- 是否允许自动合并到远端 `main`
- 是否允许自动关闭 child issue 并更新 tracking

推荐默认值：

- 以上全部允许

### 5. 暂停条件

只有命中这些条件时，主 agent 才暂停向用户请求新决策：

- 需要新 sibling issue
- 需要更新 `ADR`、`runbook` 或 `PHASE1_FREEZE`
- 必须修改 `forbidden_files`
- 推荐方案的前提被仓库现状推翻
- 连续失败超过阈值仍不收敛

推荐默认值：

- `pause_only_on = [sibling_issue_required, adr_or_runbook_change_required, phase_boundary_conflict, forbidden_file_change, repeated_nonconverging_failures]`

### 6. 汇报策略

- 是否每个 issue 完成都汇报
- 是否只在 blocked 时汇报
- 是否允许中间过程静默执行

推荐默认值：

- issue 完成时汇报
- blocked 时立即汇报
- 中间实现过程默认静默，不再为普通分歧停下确认

### 7. 推荐的授权对象

主 agent 在拿到用户确认后，应生成并持久化一个授权对象，后续派发都引用该对象：

```json
{
  "approval_bundle_id": "exec-2026-03-19-001",
  "approved_by_user": true,
  "approval_scope": "issues_30_to_33",
  "execution_mode": "proceed_with_recommended_defaults",
  "issue_parallelism": 1,
  "write_agents_per_issue": 1,
  "read_only_sidecars_per_issue": 2,
  "merge_policy": "auto_merge_main",
  "close_policy": "auto_close_child_and_update_tracking",
  "pause_only_on": [
    "sibling_issue_required",
    "adr_or_runbook_change_required",
    "phase_boundary_conflict",
    "forbidden_file_change",
    "repeated_nonconverging_failures"
  ],
  "reporting_policy": "issue_completion_or_blocked_only",
  "model": "gpt-5.4",
  "reasoning_effort": "xhigh"
}
```

### 8. 标准确认话术

主 agent 推荐使用固定话术一次性确认：

“我将按 `ISSUE_HIERARCHY.md` 顺序连续推进指定 issues，默认采用推荐方案，自动认领、派发、验证、review、合并和关闭；只有在需要新 sibling issue、需要修改 ADR/runbook/Phase 边界、必须触碰 forbidden files、或连续失败不收敛时才暂停向你确认。其余情况不中断执行。”

用户一旦回复“按推荐值执行”，主 agent 即可把该确认写成授权对象，后续不再重复发起用户级方案确认。

### 9. 可直接使用的确认模板

主 agent 可以直接向用户发送下面这份模板，一次性完成执行授权确认：

```md
## 执行确认单

### 1. 执行范围
- 连续推进：`#30 -> #33`
- 顺序规则：严格按 `ISSUE_HIERARCHY.md`
- blocked 策略：不自动跳过

### 2. 默认决策
- 未单独点名的实现分歧：默认采用主 agent 推荐值
- subagent：收到已批准方案后直接执行，不再二次确认

### 3. 并发规则
- issue 级别：严格串行
- issue 内部：`1` 个 writer + 最多 `2` 个只读 sidecar

### 4. 自动化权限
- 自动认领 issue：允许
- 自动创建 worktree / branch：允许
- 自动派发 subagent：允许
- 自动 review / verification：允许
- 自动合并到远端 `main`：允许
- 自动关闭 child issue 并更新 tracking：允许

### 5. 暂停条件
仅在以下情况暂停并请求新决策：
- 需要新 sibling issue
- 需要更新 `ADR` / `runbook` / `PHASE1_FREEZE`
- 必须修改 `forbidden_files`
- 推荐方案前提被仓库现状推翻
- 连续失败超过阈值仍不收敛

### 6. 汇报策略
- issue 完成时汇报
- blocked 时立即汇报
- 普通实现过程不中断

### 7. 模型要求
- 主 agent：`gpt-5.4` + `xhigh`
- subagent：`gpt-5.4` + `xhigh`

如果以上按推荐值执行，请直接回复：

`按推荐值执行`
```

用户确认后，主 agent 应立刻生成对应的授权对象并在后续所有派发中引用，而不是再次向用户确认普通实现分歧。

### 10. `approval_bundle` 数据结构

推荐把用户的一次性确认持久化为独立的授权对象，而不是混在 runtime state 里。

建议文件：

- `D:/fqcex/.codex/orchestrator/approval_bundle.json`

建议定义：

```python
@dataclass(frozen=True)
class ApprovalBundle:
    bundle_id: str
    approved_by_user: bool
    approved_at: str
    scope_label: str
    issue_start: int
    issue_end: int
    execution_mode: str
    issue_parallelism: int
    write_agents_per_issue: int
    read_only_sidecars_per_issue: int
    merge_policy: str
    close_policy: str
    reporting_policy: str
    pause_only_on: tuple[str, ...]
    recommended_defaults: tuple[str, ...]
    model: str
    reasoning_effort: str
```

推荐原因：

- 用户一次确认后可跨多个 issue 复用
- 不会和当前运行态互相污染
- 主 agent 可明确校验授权范围和自动化权限

### 11. `approval_bundle` 与 runtime state 的关系

推荐拆成两个文件：

- `approval_bundle.json`：保存用户授权
- `state.json`：保存当前执行现场

`state.json` 只引用：

- `approval_bundle_id`

推荐结构：

```json
{
  "approval_bundle_id": "exec-2026-03-19-001",
  "active_issue_id": 30,
  "status": "implementing",
  "active_branch": "codex/issue-30-...",
  "active_worktree": "D:/fqcex/.worktrees/issue-30-...",
  "owner_agent_id": "agent-123",
  "head_sha": "abc123"
}
```

这样切 issue 时不需要重建授权，清理运行态也不会误删用户确认。

### 12. CLI 入口

推荐增加授权相关子命令：

- `py scripts/issue_orchestrator.py approval create --issue-start 30 --issue-end 33`
- `py scripts/issue_orchestrator.py approval show`
- `py scripts/issue_orchestrator.py approval check --issue 31`

默认行为：

- 自动使用推荐值
- 自动生成 `bundle_id`
- 自动写入 `approval_bundle.json`

只有确实需要覆盖默认值时，才允许通过少量可选参数修改。

### 13. 主 Agent 使用规则

主 agent 每次推进新 issue 前，都必须检查：

- issue 是否落在 `approval_bundle` 授权范围内
- 模型是否仍是 `gpt-5.4`
- `reasoning_effort` 是否仍是 `xhigh`
- 并发参数是否仍满足单 writer 约束
- merge / close policy 是否允许自动执行

只要任一不满足，就不能继续自动推进。

这保证了“一次确认”在后续执行中不是一句口头约定，而是一个可校验的执行契约。

## 默认参数

- `issue_parallelism = 1`
- `write_agents_per_issue = 1`
- `read_only_sidecars_per_issue = 2`
- `model = gpt-5.4`
- `reasoning_effort = xhigh`

## 成功标准

实现完成后，系统应满足：

- 主 agent 能稳定选出唯一正确的下一个 child issue
- 主 agent 能阻止越序开发
- 主 agent 能在不破坏顺序的前提下启用必要并发
- subagent 写入权始终唯一
- 验收、merge 和 close 只能由主 agent 执行
- runtime state 可恢复和追踪
