# Live Readiness 与 Canary 阶段设计

## 背景

当前仓库已经完成：

- Phase 1：单交易所 runtime / recovery / reconciliation 闭环
- Phase 2：三交易所基线、Supervisor、PostgreSQL 真相存储
- Phase 3：checker、fault injection、`repository-scoped` dry run
- Phase 4：control plane / audit / operator boundary 的文档冻结

但当前主线仍未正式声明：

- 真实交易所 `live/testnet` 连接验证完成
- 真实小资金下单与成交链路完成验证
- 真实订单、仓位、余额对账链路完成验证
- 真实 operator action / audit / rollback 闭环完成验证

因此，现有 roadmap 在“平台化设计”与“原生适配器策略”之间缺少一个专门用于真实交易验收的阶段。

## 目标

新增一个独立阶段，用于在当前 `NautilusTrader + Supervisor + PostgreSQL + Checker` 主链路不变的前提下，完成三交易所 `USDT` 线性永续的小资金 `live` canary 验收。

该阶段的目标是：

- 落地最小 control-plane backend
- 落地真实 operator action 与 audit query 闭环
- 落地 live 环境、安全闸门、preflight、rollback 口径
- 补充最小 operator UI，服务人工验收
- 完成 `Bybit`、`Binance`、`OKX` 三家 venue 的小资金 live canary
- 输出正式 closeout、残余风险和放量建议

## 非目标

本阶段不负责：

- native adapter 替换
- 多账户与高可用
- 长尾交易所扩展
- 完整生产后台或通用运营平台
- 将 canary 结论升级解释为大规模放量许可

## 方案比较

### 方案 A：直接在现有成果上补 live canary

优点：

- 路径最短

缺点：

- 会把 control-plane 实现、live 安全闸门、前端、真实 canary 和 closeout 混成一次交付
- 作用边界不清，主 agent 编排难度高

### 方案 B：新增独立 `Live Readiness / Canary` 阶段

优点：

- 贴合当前仓库真实现状
- 将“平台化设计”与“真实 live 验收”分离
- 便于主 agent 严格按 child issue 顺序推进
- 前端可以建立在真实 read models 和 operator actions 之上

缺点：

- 需要新增一个 epic 和多组 tracking / child issues

### 方案 C：先做原生适配器，再做 live

优点：

- 长期技术路径更纯

缺点：

- 将真实交易验收不必要地延后
- 同时引入适配器替换风险，不利于最小 live 验收

## 推荐方案

采用方案 B：

- 在当前 Phase 4 后新增独立阶段：`Live Readiness 与 Canary 验收`
- 将现有 Phase 5、Phase 6 顺延为新的 Phase 6、Phase 7

## NautilusTrader 的使用口径

新增阶段不改变已冻结的 truth ownership。

`NautilusTrader` 继续承担：

- venue connectivity
- execution
- reconciliation
- order / position / balance truth

`Supervisor` 继续承担：

- tradeability truth
- `LIVE / DEGRADED / RESYNCING / REDUCE_ONLY / BLOCKED` 决策

`Control Plane` 继续承担：

- 只读投影视图
- 受控 operator request surface

`Audit` 继续承担：

- append-only trail
- operator action / recovery / supervisor state change 留痕

本阶段不把 `NautilusTrader` 扩展成：

- 新的 tradeability truth source
- control-plane 平台中心
- 审计系统
- 原生适配器替换入口

## 阶段结构

推荐拆成 3 个 tracking。

### Tracking A：最小控制平面与审计查询实现

目标：

- 将 Phase 4 已冻结的 control-plane / audit 边界落成最小可运行 backend

建议 child issues：

1. 控制平面实现：增加只读 HTTP 服务骨架与 health/readiness
2. 控制平面实现：落地 venue / instrument / recovery / checker 读模型查询接口
3. 控制平面实现：落地 operator action 写接口与前提校验
4. 控制平面实现：落地 audit event 查询接口与相关测试

### Tracking B：live 环境、安全闸门与 operator UI

目标：

- 为真实小资金 canary 提供最小可执行安全闭环
- 提供供人工验收使用的最小 operator UI

建议 child issues：

5. live 部署：定义 production-like env、secrets、host runbook 与 preflight
6. live 安全闸门：实现 max notional、最小交易对 allowlist、kill switch 与 operator approval
7. operator UI：增加只读验收控制台与 tradeability / recovery / audit 页面
8. operator UI：增加受控 operator action 页面与审计联动验证

### Tracking C：三交易所 live canary 与 closeout

目标：

- 在真实环境下完成三交易所小资金 canary
- 产出正式 closeout

建议 child issues：

9. live canary：执行 Bybit 单账户小资金验收并收集证据
10. live canary：执行 Binance 单账户小资金验收并收集证据
11. live canary：执行 OKX 单账户小资金验收并收集证据
12. live canary：输出三交易所 closeout、残余风险与放量建议

## 前端插入点

前端不应在当前阶段立即启动，也不应等到所有 canary 结束后再补。

推荐插入点：

- 在 Tracking A 完成最小 backend 之后
- 在 Tracking B 的 live preflight / safety gate 就绪之后
- 再开始 `operator UI` 相关 child issues

前端第一版只负责：

- 查看 venue / instrument tradeability
- 查看 recovery runs
- 查看 audit events
- 发起受控 operator action
- 服务 live canary 和 closeout 的人工验收

不负责：

- 大规模运营后台
- 多租户
- 高级图表系统
- 完整权限中心

## 退出条件

### Tracking A 退出条件

- control-plane backend 可运行
- venue / instrument / recovery / checker / audit 读接口可查询
- operator action 写接口具备前提校验
- 接口级与最小集成测试通过

### Tracking B 退出条件

- secrets / env / host runbook / preflight 明确
- max notional / allowlist / kill switch / operator approval 生效
- operator UI 可支持人工验收与最小动作闭环

### Tracking C 退出条件

- `Bybit`、`Binance`、`OKX` 三家都完成小资金 live canary
- 每家均有 operator approval、订单/仓位/余额对账、审计 trail 和必要 rollback 证据
- 有统一 closeout
- closeout 明确覆盖范围、残余风险和放量建议

### 阶段退出条件

只有在 Tracking A、B、C 全部完成后，才关闭本阶段 epic。

本阶段完成口径定义为：

- 三交易所
- 单账户
- 小资金
- 受控 allowlist
- 有 operator / audit / reconciliation / rollback 证据

而不是：

- 生产大规模放量许可

## 治理与文档更新

本设计落地后，应同步更新：

- `docs/roadmap/ROADMAP.md`
- `docs/roadmap/ISSUE_HIERARCHY.md`
- `docs/architecture/ARCHITECTURE.md`
- `docs/memory/PROJECT_STATE.md`
- `docs/memory/ACTIVE_WORK.md`
- `docs/memory/SESSION_HANDOFF.md`

同时新增：

- 一个新的 epic
- 3 个新的 tracking
- 12 个新的 child implementation issues

并将原有 Phase 5、Phase 6 顺延为新的 Phase 6、Phase 7。
