# PROJECT_STATE

## 项目目标

`fqcex` 是一个面向多交易所永续合约套利的连接管理平台。

## 当前主线状态

- 本地 `main` 已与 `origin/main` 对齐。
- 当前远端主线最新提交为 `7ed2793291ab9dc64d45c597905deead0e292408`。
- GitHub 上已完成并关闭：
  - Phase 1 epic `#2`
  - Phase 2 epic `#3`
  - Phase 3 epic `#4`
  - Phase 4 epic `#5`

## 冻结范围

- 交易所：`Bybit`、`Binance`、`OKX`
- 产品范围：`USDT` 线性永续
- 主 runtime：`NautilusTrader`
- 交易可用性真相源：`Supervisor`
- 独立公共行情校验：`Cryptofeed`

## 当前主线已完成能力

### Phase 1

- `perp_platform` Python 包、入口点、配置契约、共享测试基座
- 统一合约标识、市场枚举、数量归一化与 OKX 张数换算
- Bybit 运行时初始化、恢复、对账、`REDUCE_ONLY / BLOCKED` 投影
- Codex cloud 仓库迁移与主 agent / cloud dry run 基座

### Phase 2

- Supervisor 状态机、触发器、交易所级与交易对级投影
- PostgreSQL truth schema、订单 / 仓位 / 余额 / 可交易性 / 恢复仓储
- Binance USDⓈ-M 基线运行时与恢复退避
- OKX USDT 永续运行时、张数换算与约束回归

### Phase 3

- Cryptofeed checker bootstrap、feeds、policies、signals
- 故障注入工具：
  - `inject_ws_disconnect.py`
  - `inject_private_silence.py`
  - `inject_reconcile_diff.py`
- 干跑配置、安全闸门、审计采集
- `repository-scoped` BTC / ETH 干跑证据与 closeout：
  - `docs/plans/dry-run-evidence.md`
  - `docs/plans/dry-run-closeout.md`

### Phase 4

- control-plane API 表面、operator actions、tradeability / recovery 读模型边界
- audit event、audit storage、retention / redaction / access control 约束
- operator force resume / audit checklist 等运行手册边界

## 运行边界说明

- Phase 3 的干跑结论只覆盖 `repository-scoped` 受控演练。
- 当前主线**不**声称真实交易所 `live/testnet` 演练、真实下单或真实资金路径已完成验证。

## 下一阶段

- 下一个待执行 epic 是 Phase 5：`#141 [史诗] 第 5 阶段：Live Readiness 与 Canary 验收`
- 当前顺序入口是 `#142 [跟踪] 落地最小控制平面与审计查询`
- 第一个 ready child issue 是 `#145 控制平面实现：增加只读 HTTP 服务骨架与 health/readiness`
