# Operator UI 人工验收实用手册

## 目的

这份手册面向人工验收人，说明如何通过当前已经上线的前端页面，验收第 5 阶段里**已经实现**的 UI 能力。

这份手册只覆盖：

- 前端页面是否可访问
- 页面是否展示当前约定的验收数据
- 页面上的最小交互是否符合当前设计

这份手册**不**覆盖：

- 真实交易所 live canary 已完成
- 真实 operator write API 已开放
- 真实控制平面读接口已作为前端数据源接入

## 访问入口

当前公网入口：

- `http://38.60.236.47:4173/`
- `http://38.60.236.47:4173/actions`

推荐从首页进入后，依次验收：

1. `Tradeability`
2. `Recovery`
3. `Audit`
4. `Actions`

## 当前验收边界

当前前端用于 **Phase 5 人工验收与 closeout 演示**，数据来源仍是静态 adapter / fixture，不是实时控制平面后端。

因此你在页面上看到的内容，当前可以证明的是：

- 页面结构已经实现
- 状态展示逻辑已经实现
- 最小交互和前提条件 gating 已经实现
- action 提交后的 audit echo 联动已经实现

但当前**不能**据此证明：

- 真实交易所状态已经被实时接入
- 页面上的 action 已经写入真实 control-plane
- Bybit / Binance / OKX 的 live canary 已经执行完成

## 验收前准备

开始前建议记录：

- 验收时间
- 验收人
- 访问入口
- 当前看到的页面截图
- 是否发现与手册不一致的行为

## 页面 1：Tradeability

访问：

- `http://38.60.236.47:4173/tradeability`

### 你要看什么

页面应分成两块：

1. `Venue Tradeability`
2. `Instrument Tradeability`

### 验收步骤

1. 打开页面，确认左侧导航存在 `Tradeability / Recovery / Audit / Actions`
2. 在 `Venue Tradeability` 卡片区，确认能看到 3 个 venue：
   - `BYBIT`
   - `BINANCE`
   - `OKX`
3. 确认每个 venue 都有：
   - 状态 badge
   - 原因说明
   - `Allow Open`
   - `Allow Reduce`
4. 在表格区确认当前展示了冻结范围内的 instrument tradeability 数据

### 当前预期结果

- `BYBIT` 状态为 `LIVE`
- `BINANCE` 状态为 `DEGRADED`
- `OKX` 状态为 `REDUCE_ONLY`
- 表格中至少能看到：
  - `BTC-USDT-PERP`
  - `ETH-USDT-PERP`

### 这证明了什么

- 前端已经能把 venue 级和 instrument 级可交易性分开展示
- 页面已经具备 closeout 所需的核心只读视图

### 这不能证明什么

- 这些状态当前不是实时 Supervisor 真相
- 不能据此声称真实交易已放行

## 页面 2：Recovery

访问：

- `http://38.60.236.47:4173/recovery`

### 你要看什么

页面应展示 recovery run 时间线卡片。

### 验收步骤

1. 打开页面，确认标题为 `Recovery Runs`
2. 确认页面中至少有 2 个 recovery run 卡片
3. 每个卡片应包含：
   - `runId`
   - `status`
   - `phase`
   - `triggerReason`
   - `blockersJson`

### 当前预期结果

- 存在一个 `ready` 的 recovery run
- 存在一个 `running` 的 recovery run
- 至少有一个 run 的 `blockersJson` 中出现 `awaiting operator approval`

### 这证明了什么

- 前端已经能承载 recovery / reconciliation 的 closeout 展示位
- 页面可以让验收人看到“已就绪”和“仍在阻塞”的差异

### 这不能证明什么

- 当前 recovery run 不是实时从后端拉取
- 不代表真实 venue 恢复已经完成

## 页面 3：Audit

访问：

- `http://38.60.236.47:4173/audit`

### 你要看什么

页面应展示 audit 时间线，并带一个过滤输入框。

### 验收步骤

1. 打开页面，确认标题为 `Audit Events`
2. 确认顶部有过滤输入框，placeholder 包含 `corr-live-001`
3. 默认情况下应看到多条 audit event
4. 在过滤框输入：
   - `corr-live-001`
   - 或 `approve_live_canary`
5. 确认列表会收敛到匹配项

### 当前预期结果

默认至少能看到这些事件类型之一：

- `approve_live_canary`
- `recovery_completed`

并且能看到：

- `correlationId`
- `sourceComponent`
- `venue`
- `instrumentId`（如果该事件有 instrument scope）

### 这证明了什么

- 前端已经具备最小 audit timeline 展示能力
- 前端已经具备最小的 audit filter 行为

### 这不能证明什么

- 当前并不是在查询真实 audit store
- 不能据此声称真实 live 审计链已打通

## 页面 4：Actions

访问：

- `http://38.60.236.47:4173/actions`

### 你要看什么

页面应包含两部分：

1. 上方 target 状态卡片
2. 下方 action form + audit echo

### 当前支持的最小 action

- `force_reduce_only`
- `force_block`
- `force_resume`

### 验收步骤 A：查看 target 前提条件

1. 确认页面上存在至少 3 个 target：
   - `BYBIT:BTC-USDT-PERP`
   - `BINANCE:ETH-USDT-PERP`
   - `OKX:BTC-USDT-PERP`
2. 确认每个 target 卡片显示：
   - `recoveryReady`
   - `approvalRecorded`
   - `killSwitchInactive`
   - `allowReduce`

### 验收步骤 B：验证按钮禁用逻辑

1. 不填写 `Reason`
2. 任意选择一个 action
3. 确认 `Submit Action` 按钮保持禁用

这一步应证明：

- 页面已经实现基础前提条件 gating

### 验收步骤 C：验证 `force_resume` 的受限行为

1. 选择 target：`OKX:BTC-USDT-PERP`
2. 选择 action：`force_resume`
3. 输入任意 `Reason`
4. 观察 preconditions 列表

### 当前预期结果

- 由于 `approvalRecorded = no`
- `Submit Action` 应保持禁用

这一步应证明：

- `force_resume` 不是无条件可点的
- 页面已经展示更严格的前提条件约束

### 验收步骤 D：验证可提交 action

1. 选择 target：`BYBIT:BTC-USDT-PERP`
2. 选择 action：`force_block`
3. 输入 `Reason`
4. 确认按钮变为可点击
5. 点击 `Submit Action`

### 当前预期结果

- 页面成功接受提交
- 右侧 `Audit Echo` 区域新增一条事件
- 新事件包含：
  - action 名
  - 时间
  - `correlationId`
  - venue / instrument

### 这证明了什么

- 页面已经实现：
  - target 选择
  - action 选择
  - reason 必填
  - 前提条件 gating
  - action -> audit echo 联动

### 这不能证明什么

- 当前提交并没有写入真实后端
- 只是当前阶段的前端验收闭环，不是 live operator action 已上线

## 建议的人工验收结论写法

建议你在验收记录里使用类似表述：

> 已确认 operator UI 当前可访问，并已实现 `Tradeability`、`Recovery`、`Audit`、`Actions` 四个页面的最小人工验收闭环。  
> 已验证页面展示、过滤、前提条件 gating、以及 action -> audit echo 联动行为。  
> 当前页面仍为静态验收数据驱动，不据此声称真实 control-plane 写接口或真实 live canary 已完成。

## 可勾选清单

- [ ] 已打开公网 UI 首页
- [ ] 已确认左侧导航包含 `Tradeability / Recovery / Audit / Actions`
- [ ] 已在 `Tradeability` 页面确认 3 个 venue 状态卡片
- [ ] 已在 `Tradeability` 页面确认 instrument 表格存在
- [ ] 已在 `Recovery` 页面确认 recovery run 卡片展示正常
- [ ] 已在 `Audit` 页面确认过滤输入框可用
- [ ] 已在 `Audit` 页面验证 `correlationId` 或事件类型过滤
- [ ] 已在 `Actions` 页面验证“无 reason 时按钮禁用”
- [ ] 已在 `Actions` 页面验证某个 target 上 `force_resume` 仍受前提条件限制
- [ ] 已在 `Actions` 页面验证一次可提交 action 的 audit echo
- [ ] 已记录页面截图或文字证据
- [ ] 已明确当前验收不等于真实 live canary 已完成

## 相关文档

- [Operator Readonly UI Runbook](D:/fqcex/docs/runbooks/operator-readonly-ui.md)
- [Live Canary 部署验收手册](D:/fqcex/docs/runbooks/live-canary-acceptance.md)
- [Live Canary 部署 Runbook](D:/fqcex/docs/runbooks/live-canary-deploy.md)
