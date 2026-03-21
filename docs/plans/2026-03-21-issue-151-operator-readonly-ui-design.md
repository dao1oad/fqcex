# Issue 151 Operator Readonly UI 设计

## 背景

当前仓库已经有：

- `#146` 的 tradeability / recovery / checker read models
- `#148/#162` 的 audit query surface
- `#149/#150` 的 live deploy 与 safety gate 边界

但还没有任何正式前端工程。`#151` 的目标是交付一个最小只读 operator 验收控制台，服务人工 closeout 与阶段验收。

## 方案比较

### 方案 A：React + Vite + React Router 的只读控制台，推荐

优点：

- 为后续 `#152` 写动作页保留自然扩展位
- 路由和只读适配层边界清晰
- 可以直接用 Playwright 做真实页面验收

### 方案 B：纯静态 HTML fixture 扩展

不推荐：

- 很快会在 `#152` 返工
- 不适合作为后续 operator UI 的基础

### 方案 C：直接接 Python HTTP server 做全链路前后端

不推荐：

- 超出 `#151`
- 当前 issue 只需要只读验收台，不需要把 transport 一次性接实

## 推荐方案

采用方案 A。

## 设计

### 技术选型

- `apps/control-plane-ui`
- `React 19`
- `Vite`
- `React Router`
- 原生 CSS variables + 明确视觉系统

第一版不引入：

- 写动作表单
- 认证
- 真实 API fetch

### 数据适配

增加一个静态 adapter 层，直接提供符合当前 control-plane 契约的 fixture 数据：

- venue tradeability
- instrument tradeability
- recovery runs
- audit events

后续 `#152+` 再替换成真实 HTTP adapter。

### 页面结构

最小页面：

- `/tradeability`
- `/recovery`
- `/audit`

公共 shell：

- 左侧导航
- 顶部阶段说明
- closeout 说明卡片

### 视觉方向

采用审计台 / 运维台风格：

- `IBM Plex Sans` + `IBM Plex Mono`
- 冷灰底 + 琥珀/青绿/锈红状态色
- 信息密度中高
- 强调状态、证据、时间线，不做交易终端式花哨大屏

### E2E

沿用现有 Playwright：

- 新增 operator readonly UI spec
- 用 Vite dev server 作为 Playwright webServer

## 非目标

- 不实现 operator action 页面
- 不实现真实 audit 查询筛选后端
- 不做完整 design system 文档化

## 文档更新

同步更新：

- `README.md`
- `docs/runbooks/operator-readonly-ui.md`
