# #152 Operator Action UI 设计

## 目标

在现有只读 operator UI 基础上补一页最小受控 action 页面，展示 action 前提、禁用不满足前提的提交，并把成功提交的 action 作为新的 audit event 回显到 UI 中，供人工验收使用。

## 边界

本 issue 只做：

- `apps/control-plane-ui` 内的最小 action 页面
- 静态 adapter 驱动的前提校验展示
- action 提交后的本地 audit timeline 回显
- Playwright E2E 和 runbook 更新

本 issue 不做：

- 真实 HTTP 写接口接入
- 认证、RBAC、多用户审批
- 复杂运营后台

## 方案对比

### 方案 A：只做静态只读 action 文案

- 在 `/actions` 放几块说明卡
- 不做表单，不做 audit 联动

缺点：

- 无法证明“只有满足前提的 action 才可提交”
- 不满足 issue 的验收标准

### 方案 B：最小交互式 action 页面，推荐

- 提供目标选择、action 选择、理由输入
- 根据 fixture 计算前提是否满足
- 未满足时禁用提交并展示原因
- 满足时可提交，并把 event 注入现有 audit timeline

优点：

- 满足 issue 验收标准
- 不抢跑真实 control-plane 写接口
- 后续接真实 API 时只需替换 adapter

### 方案 C：直接接真实 control-plane operator action API

缺点：

- 会把 `#152` 与后端部署/权限问题耦合
- 对当前人工验收 UI 来说超配

## 推荐设计

采用方案 B。

### 信息架构

- 侧边栏新增 `Actions`
- `/actions` 页面分三块：
  - `Action Targets`：展示可操作目标及当前 supervisor 状态
  - `Action Form`：选择 action、目标、理由
  - `Audit Echo`：显示本会话最新 action 写入的审计事件

### 数据流

- `Shell` 持有共享的 `auditTimeline` 状态，初始值来自静态 `auditEvents`
- `AuditPage` 从共享状态读取事件
- `ActionsPage` 提交成功后通过共享更新函数追加新 audit event
- 更新时使用 `startTransition`，避免让表单提交与时间线渲染耦在同步路径里

### 最小前提模型

- `force_reduce_only`
  - 需要目标允许 `reduce`
- `force_block`
  - 只需要填写理由
- `force_resume`
  - 需要：
    - `recoveryReady`
    - `approvalRecorded`
    - `killSwitchInactive`
    - 当前状态不是 `LIVE`

### Fixture 口径

- `BYBIT BTC-USDT-PERP`
  - 当前 `LIVE`
  - 适合展示 `force_resume` 禁用
- `BINANCE ETH-USDT-PERP`
  - 当前 `DEGRADED`
  - 满足 `force_resume` 前提，可成功提交
- `OKX BTC-USDT-PERP`
  - 当前 `REDUCE_ONLY`
  - `approvalRecorded = false`
  - 用于展示前提不满足

## 验证

- 新增 Playwright 用例：
  - 访问 `/actions`
  - 验证不满足前提时提交按钮 disabled
  - 切换到满足前提的目标/action 后提交成功
  - 跳转或切换到 `Audit` 页面后能看到新 event
- 继续跑：
  - `npm --prefix apps/control-plane-ui run build`
  - `npx playwright test tests/e2e`
  - `py -m pytest tests -q`
