# fqcex Issue 分层细化与治理设计

## 背景

当前仓库已经建立了 roadmap epics（`#2` 到 `#7`）和一组按 phase 划分的 feature issues（`#10` 到 `#23`）。这些 issue 对路线是够用的，但粒度仍然偏粗，无法直接作为后续 subagent 的稳定编码边界：

- 单个 issue 经常同时覆盖模型、运行时、测试、文档、集成多个维度。
- “Done Criteria” 适合阶段验收，不适合直接交给一个 subagent 执行。
- 目前没有清晰的 issue 分层规则，后续容易出现直接从 epic 或粗 issue 开始编码的情况。

因此需要在不破坏现有 roadmap 结构的前提下，对 backlog 做一次系统性分层细化。

## 目标

建立一套明确的 issue 层级与治理规则，让后续工作遵循下面的执行路径：

`Epic -> Tracking Parent Issue -> Child Implementation Issue -> PR`

并满足：

- 每个 child issue 都能独立交给一个 subagent 执行。
- 每个 child issue 都有明确边界、依赖、非目标、验收和验证方式。
- 父 issue 保留阶段能力视角，不再直接作为编码入口。
- 项目治理文档明确规定 issue 层级、关闭规则和 subagent 使用规则。

## 非目标

- 不重做现有 roadmap phase 结构。
- 不关闭 roadmap epics。
- 不把全部 backlog 扁平化成几十个彼此无父子关系的碎 issue。
- 不在这次工作里实现这些 issue 对应的代码。

## 方案对比

### 方案 A：只增强现有粗 issue

直接重写 `#10` 到 `#23` 的正文，不新增子 issue。

优点：

- 结构最稳定
- issue 数量不增加

缺点：

- 单个 issue 仍然太大
- 不适合后续逐个交给 subagent 编码

### 方案 B：保留粗 issue 为 tracking parent，再拆 child issues

做法：

- roadmap epic 保持不变
- 现有 feature issue 保留，但改造成 tracking parent
- 为每个 tracking parent 新建 2 到 6 个 child implementation issues

优点：

- 保留 roadmap 和阶段能力视图
- child issue 可以做到真正的 subagent-ready
- 关闭规则清晰

缺点：

- issue 数量会增加
- 需要补一套治理规则避免层级混乱

### 方案 C：只保留 epic，粗 issue 直接关闭，全部重建子 issue

优点：

- 最终 backlog 最干净

缺点：

- 会丢失当前 feature issue 作为能力块的中间层
- roadmap 到编码任务之间跨度过大
- 后续验收不方便

## 选型结论

采用 **方案 B**。

最终层级固定为：

- `Epic`：阶段目标与退出条件
- `Tracking Parent Issue`：单个能力块的边界、依赖、总验收、child checklist
- `Child Implementation Issue`：可直接交给 subagent 执行的最小实现/设计/集成任务

## Issue 层级设计

### 1. Epic

职责：

- 表达 roadmap phase 的业务/平台目标
- 聚合 tracking parents
- 定义阶段退出条件

规则：

- 保持 `type/epic`
- 不直接作为编码入口
- 只在所有 tracking parents 完成后关闭

### 2. Tracking Parent Issue

对应当前的 `#10` 到 `#23`。

职责：

- 表达一个完整能力块
- 聚合 child issues
- 说明整体边界、依赖和父级验收

规则：

- 标题前缀改为 `[Tracking]`
- 标签从 `type/feature` 改为 `type/tracking`
- 正文必须包含：
  - 父 epic
  - 能力目标
  - 任务边界
  - 非目标
  - 依赖
  - child issue checklist
  - 关闭条件
- 不直接派给 subagent 编码
- 只有在 child issues 全部关闭且父 issue 自身验收满足后才关闭

### 3. Child Implementation Issue

职责：

- 作为单个 subagent 的直接工作单元
- 一次只做一个清晰目标

规则：

- 使用新标签 `type/task`
- 保留 `phase/*` 与 `area/*`
- 正文必须包含：
  - 父 tracking issue
  - 父 epic
  - Objective
  - Scope
  - Out of Scope
  - Dependencies
  - Deliverables
  - Acceptance Criteria
  - Verification
  - Close Rule
- 一个 child issue 原则上只允许一个 subagent 拥有
- 若执行中发现 scope 扩大，应新开 sibling child issue，不得直接膨胀原 child issue

## 命名与标签设计

### 标题规范

- Epic：保留现状，如 `[Epic] Phase 3 - Checker and Dry Run`
- Tracking Parent：`[Tracking] <能力块标题>`
- Child Issue：`<能力块>: <单一子任务>`

### 标签规范

- `type/epic`
- `type/tracking`
- `type/task`
- 继续保留 `phase/*`
- 继续保留 `area/*`

父 issue 与 child issue 都保留对应的 `phase/*` 和 `area/*`，这样既能按阶段看，也能按领域看。

## Child Issue 的粒度规则

为了让后续 subagent 编码边界明确，child issue 必须满足：

- 最好对应一个目录或一组强相关文件
- 最多只做一个主要产物：
  - 一个模型层
  - 一个运行时接入块
  - 一个恢复逻辑块
  - 一个存储块
  - 一个测试/验证块
  - 一个设计/接口定义块
- 不同时跨“核心实现 + 大量运维文档 + 多交易所联调”三种维度

## 关闭规则

- Child Issue：
  - 代码/文档/验证完成后立即关闭
- Tracking Parent：
  - 所有 child issue 完成
  - 父 issue 的整体 Done Criteria 满足
  - 之后再关闭
- Epic：
  - 所有 tracking parents 完成
  - phase 退出条件满足
  - 之后再关闭

## 子任务拆分原则

这次细化按下面原则拆分：

- Phase 1 / 2 的 issue 以“可编码实现单元”为主
- Phase 3 混合“实现 + 运行验证 + 报告”
- Phase 4 / 5 / 6 仍以“设计与平台边界定义”为主，但每个 child issue 仍保持单一目标

## 治理文档更新范围

这次工作完成后，至少要更新：

- `GOVERNANCE.md`
- `CONTRIBUTING.md`
- `AGENTS.md`

新增或明确：

- issue 三层结构
- 不允许直接从 epic / tracking parent 开始编码
- subagent 只能接 child issue
- 关闭规则
- scope 扩张时的开新 issue 规则

## 预期结果

完成后，仓库将具备：

- 清晰的 roadmap -> tracking -> implementation 层级
- 每个 implementation issue 都能被独立派发
- 后续编码能以 issue 为稳定单位推进，而不是在聊天中反复重新切 scope
