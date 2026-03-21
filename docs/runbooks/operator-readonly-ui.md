# Operator Readonly UI Runbook

## 目的

提供第 5 阶段人工验收使用的最小只读控制台，用于查看：

- venue / instrument tradeability
- recovery runs
- audit events
- 受控 operator actions 与 audit echo

## 当前边界

该 UI 当前只消费静态 adapter 数据，用于人工 closeout 演示和验收。

它当前不负责：

- 真实 HTTP operator write
- 真实 HTTP control-plane fetch
- 认证与权限控制

## 启动方式

先安装前端依赖：

```sh
npm --prefix apps/control-plane-ui install
```

启动开发服务器：

```sh
npm --prefix apps/control-plane-ui run dev -- --host 127.0.0.1 --port 4173
```

## 页面

- `/tradeability`
- `/recovery`
- `/audit`
- `/actions`

## Action 页面验收口径

`/actions` 页面当前仍是静态 adapter 驱动，但它已经覆盖第 5 阶段最小 operator action 验收闭环：

- 展示目标级前提条件
- 不满足前提时禁用提交
- 满足前提时允许提交
- 提交后把 action 作为新的 audit event 回显到共享 timeline

当前支持的最小 action：

- `force_reduce_only`
- `force_block`
- `force_resume`

## E2E

运行：

```sh
npx playwright test tests/e2e/operator-readonly-ui.spec.ts
npx playwright test tests/e2e/operator-actions-ui.spec.ts
```

## Closeout 用途

这套控制台的目标不是替代真实 control-plane 或 live canary 证据，而是把当前阶段关键只读信息和最小受控 action 验收收口到一个人工入口中。
