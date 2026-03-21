# Operator Readonly UI Runbook

## 目的

提供第 5 阶段人工验收使用的最小只读控制台，用于查看：

- venue / instrument tradeability
- recovery runs
- audit events

## 当前边界

该 UI 当前只消费静态 adapter 数据，用于人工 closeout 演示和验收。

它当前不负责：

- operator write actions
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

## E2E

运行：

```sh
npx playwright test tests/e2e/operator-readonly-ui.spec.ts
```

## Closeout 用途

这套只读控制台的目标不是替代 operator action 或 live canary 证据，而是把当前阶段关键只读信息收口到一个人工验收入口中。
