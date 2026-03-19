# #89 单账号 Review 治理设计

## 背景

当前仓库已经定义了 `Reviewer` 角色、PR 模板和基础 `CODEOWNERS`，但尚未明确以下关键问题：

- 哪些改动在合并前必须完成 review
- 单账号 GitHub 协作下如何留下可审计的独立 review 证据
- 高风险目录的审查责任边界是什么
- 后续 CI / required checks 应使用什么稳定名称

按照 `docs/roadmap/ISSUE_HIERARCHY.md`，这项工作应作为 `#79 [Tracking] 收敛开发工作流与最小交付基座` 下的新 child issue 执行。对应 issue 为 `#89 评审治理：补充单账号 PR review 证据与责任边界`。

## 目标

- 为单账号协作定义最小 review 治理闭环
- 明确哪些改动必须在合并前完成 review
- 固定 PR 中的 `Review Evidence` 结构
- 细化高风险目录的 `CODEOWNERS` 边界
- 冻结后续 required checks 名称：`governance-check`、`python-check`

## 非目标

- 不直接修改 GitHub ruleset / branch protection
- 不实现 `python-check` workflow
- 不引入多账号审批模型
- 不扩展到 Docker、deploy、smoke 验证

## 方案比较

### 方案 A：只补文档规则

仅修改 `GOVERNANCE.md`、`CONTRIBUTING.md`、PR 模板。

优点：

- 改动最小
- 容易落地

缺点：

- 没有目录责任边界
- 不能为后续 required checks 提供稳定入口

### 方案 B：文档 + 仓库内执行入口

修改：

- `GOVERNANCE.md`
- `CONTRIBUTING.md`
- `.github/PULL_REQUEST_TEMPLATE.md`
- `.github/CODEOWNERS`

优点：

- 规则、执行入口、目录责任边界一致
- 全部变更都能在仓库内版本化
- 不依赖平台管理员权限

缺点：

- 仍然不能单靠仓库文件强制“第二身份审批”

### 方案 C：文档 + 平台配置

在方案 B 基础上再写入 branch protection / ruleset 的平台目标状态。

优点：

- 闭环最完整

缺点：

- 平台状态不在仓库内
- 当前单账号前提下容易把 scope 扩大为平台治理审计

## 选型

采用方案 B。

理由：当前最需要的是在单账号前提下把 review 从“口头约定”收口为“仓库内可审计流程”，而不是立刻扩展到平台治理或多账号审批。

## 设计

### 单账号下的独立 review 证据

“独立 review 证据”定义为：

- 独立于实现提交的审查步骤
- 独立记录在 PR 中
- 包含 review 范围、方法、结论、处理结果和最终验证

最小要求：

1. PR 正文必须包含 `Review Evidence` 段
2. PR 中必须额外留下 1 条独立 review comment
3. 没有 review 证据，不允许合并 PR
4. 没有 review 证据，不允许关闭对应 child issue

### Review 分级

普通改动：

- 必须有 `Review Evidence`

高风险改动：

- 状态机
- 恢复流程
- 风控规则
- 交易准入规则
- 数据模型
- 订单与持仓真相逻辑
- `docs/adr`
- `docs/runbooks`
- `.github`
- `src/`

额外要求：

- review 证据完整
- 风险说明完整
- 验证记录完整
- 文档影响完整

### 目录责任边界

`CODEOWNERS` 细化到：

- `/.github/`
- `/docs/adr/`
- `/docs/runbooks/`
- `/docs/architecture/`
- `/src/`

当前仍然指向同一账号，但用于表达目录责任边界，并为后续多账号协作预留稳定结构。

### Required Checks 名称约定

在治理文档中冻结：

- `governance-check`
- `python-check`

这里先冻结名称，不等于本 issue 直接实现 `python-check`。

## 测试策略

虽然本 issue 主要是文档和仓库配置，但仍通过轻量回归测试收口关键契约：

- 新增测试验证 `GOVERNANCE.md`、`CONTRIBUTING.md` 中存在 review 治理关键语句
- 新增测试验证 PR 模板存在 `Review Evidence`
- 新增测试验证 `CODEOWNERS` 覆盖约定的高风险目录

测试只验证稳定契约，不验证具体文案措辞。

## 风险与控制

- 风险：规则写得过强，但当前单账号无法执行
  - 控制：把“独立”定义为流程独立、证据独立，而非身份独立
- 风险：把后续 `#81` 的实现偷渡进来
  - 控制：仅冻结 required checks 名称，不实现 workflow
- 风险：测试过度绑定文案
  - 控制：只验证关键段落和约定 token，不锁死全文表述

## 验证

- `py -m pytest tests/governance/test_review_governance.py -q`
- `py -m pytest tests -q`
- 人工检查新 PR 模板是否能直接承载 review 留痕
