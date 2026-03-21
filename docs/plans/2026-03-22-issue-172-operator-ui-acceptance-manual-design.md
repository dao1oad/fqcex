# `#172` Operator UI 人工验收手册设计

## 目标

为当前已经公网可访问的 operator UI 补充一份面向验收人的实用手册，让非开发者也能按页面逐项确认系统当前已经实现的前端验收能力。

## 当前上下文

- 前端入口已开放：
  - `http://38.60.236.47:4173/`
  - `http://38.60.236.47:4173/actions`
- 当前 UI 仍以静态 adapter 数据为主，用于 Phase 5 的人工 closeout / operator acceptance 演示。
- 控制平面真实 write API 仍未对公网开放，因此 UI 的验收口径必须明确区分：
  - “可用于人工验收的已实现能力”
  - “尚未进入真实 live canary 的能力”

## 文档策略

新增独立 runbook：

- `docs/runbooks/operator-ui-acceptance-manual.md`

不把内容继续塞进：

- `docs/runbooks/operator-readonly-ui.md`

原因：

- 现有文件更偏开发/运行说明
- 新文档需要面向验收人，强调“看什么、怎么点、看到什么才算通过”

## 结构

### 1. 访问入口

- 说明公网访问地址
- 说明推荐浏览器
- 说明当前 UI 的定位和边界

### 2. 验收前说明

- 当前页面数据性质：静态验收数据
- 当前页面不能证明的事项
- 建议记录方式

### 3. 分页面验收

分别覆盖：

- `/tradeability`
- `/recovery`
- `/audit`
- `/actions`

每页都写清：

- 页面目标
- 验收步骤
- 预期结果
- 该结果证明了什么

### 4. 动作页专项说明

说明：

- `force_reduce_only`
- `force_block`
- `force_resume`

以及：

- 按钮何时应禁用
- 何时可以提交
- 提交后 audit echo 应如何变化

### 5. 验收清单

提供一份可以直接照着勾选的 checklist。

## 非目标

- 不修改前端功能
- 不增加真实 API
- 不把静态演示描述成真实 live canary 已完成
