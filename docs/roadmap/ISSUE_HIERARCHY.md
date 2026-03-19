# Issue 层级与执行规则

## 目标

本仓库的 backlog 固定采用三层结构：

- `Epic`
- `Tracking Parent Issue`
- `Child Implementation Issue`

后续任何编码、文档、集成、验证工作，都必须以 **child issue** 作为直接执行单元。

同时，GitHub issue 的标题与正文默认使用中文；文件路径、命令、标签名和必要术语可保留英文。

## 层级定义

### 1. Epic

职责：

- 表达阶段目标
- 挂接 tracking parent issues
- 定义阶段退出条件

规则：

- 使用标签 `type/epic`
- 不直接作为编码入口
- 只有在所有 tracking parent issues 完成后才关闭

### 2. Tracking Parent Issue

职责：

- 表达单个能力块的总边界
- 聚合 child implementation issues
- 定义该能力块的整体验收

规则：

- 使用标签 `type/tracking`
- 标题前缀为 `[Tracking]`
- 不直接作为 subagent 编码入口
- 只有在所有 child issues 完成后才关闭

### 3. Child Implementation Issue

职责：

- 作为单个 subagent 的直接工作边界
- 一次只做一个单一目标

规则：

- 使用标签 `type/task`
- 保留对应的 `phase/*` 和 `area/*`
- 必须写清：
  - 目标
  - 负责边界
  - 范围
  - 非目标
  - 依赖
  - 预期文件
  - 交付物
  - 验收标准
  - 验证
  - 关闭规则

## 执行规则

- 只允许从 `type/task` issue 直接开始编码。
- 不允许直接从 `type/epic` 或 `type/tracking` issue 开始编码。
- 一个 subagent 一次只拥有一个 child issue。
- 如果执行中发现 scope 膨胀，必须新开 sibling child issue，而不是扩大原 issue 边界。
- 一个 PR 最好只对应一个 child issue；确有必要跨多个 child issue 时，必须在 PR 中说明。
- 后续新增 issue、补充 issue 或编辑 issue，默认使用中文。
- 后续开发顺序以本文的阶段顺序、tracking 顺序和 child 顺序为准，不以 GitHub issue 编号大小为准；晚创建的补充 issue 必须插回对应阶段执行。

## 关闭规则

- Child Issue：
  - 代码或文档完成
  - 验证完成
  - 合并到主线后关闭
- Tracking Parent：
  - 所有 child issues 关闭
  - 父 issue 的 Done Criteria 满足
  - 然后关闭
- Epic：
  - 所有 tracking parents 关闭
  - phase 退出条件满足
  - 然后关闭

## 当前 Issue 树

### 第 1 阶段

- `#2 [Epic] 第 1 阶段：单交易所闭环`
  - `#79 [Tracking] 收敛开发工作流与最小交付基座`
    - `#80 开发工作流：修正 project memory 快照在 worktree 下的测试假设`
    - `#81 交付基座：增加面向 perp-platform 的 CI workflow`
    - `#82 交付基座：增加容器化与最小部署脚本`
    - `#83 交付基座：增加 smoke 验证与 rollback runbook`
  - `#10 [Tracking] 搭建 perp-platform 应用骨架`
    - `#25 搭建 perp-platform 应用骨架：创建 Python 包与入口点`
    - `#26 搭建 perp-platform 应用骨架：补充配置初始化契约`
    - `#27 搭建 perp-platform 应用骨架：补充共享测试基座`
  - `#11 [Tracking] 定义统一合约与数量模型`
    - `#28 统一模型：定义合约标识与市场枚举`
    - `#29 统一模型：实现数量归一化与 OKX 张数换算`
    - `#30 统一模型：文档化真相字段与架构约束`
  - `#90 [Tracking] 迁移仓库到 Codex cloud 开发环境`
    - `#95 Codex cloud 迁移：更新 issue hierarchy 与执行顺序`
    - `#91 Codex cloud 迁移：标准化仓库 setup 与 Linux 兼容入口`
    - `#92 Codex cloud 迁移：定义 environment、secrets 与网络访问约束`
    - `#93 Codex cloud 迁移：调整主 agent / orchestrator 的云端执行模式`
    - `#94 Codex cloud 迁移：完成 GitHub / Codex cloud dry run 与操作手册`
  - `#12 [Tracking] 实现 Bybit 线性永续运行时初始化`
    - `#31 Bybit 运行时初始化：增加配置与客户端启动入口`
    - `#32 Bybit 运行时初始化：接通公共流、私有流与执行客户端`
    - `#33 Bybit 运行时初始化：强制单向持仓、逐仓与订单能力约束`
    - `#34 Bybit 运行时初始化：增加启动与基础下单路径冒烟测试`
  - `#13 [Tracking] 实现 Bybit 恢复与对账闭环`
    - `#35 Bybit 恢复闭环：实现重连与重订阅顺序`
    - `#36 Bybit 恢复闭环：在回到 LIVE 前完成订单、仓位与余额对账`
    - `#37 Bybit 恢复闭环：投影 REDUCE_ONLY 与 BLOCKED 结果`
    - `#38 Bybit 恢复闭环：补充恢复场景测试与运行手册说明`

剩余建议执行顺序：
`#95 -> #91 -> #92 -> #93 -> #94 -> #32 -> #33 -> #34 -> #35 -> #36 -> #37 -> #38`

### 第 2 阶段

- `#3 [Epic] 第 2 阶段：三交易所基线`
  - `#14 [Tracking] 实现 Supervisor 可交易性状态机`
    - `#39 Supervisor 状态机：定义状态枚举与迁移契约`
    - `#40 Supervisor 状态机：实现流触发器求值逻辑`
    - `#41 Supervisor 状态机：分别投影交易所级与交易对级可交易性`
    - `#42 Supervisor 状态机：补充测试与架构文档`
  - `#15 [Tracking] 增加 PostgreSQL 真相存储 Schema`
    - `#43 PostgreSQL 真相存储：增加核心 Schema 与迁移`
    - `#44 PostgreSQL 真相存储：实现订单、仓位与余额仓储`
    - `#45 PostgreSQL 真相存储：实现可交易性与恢复持久化`
    - `#46 PostgreSQL 真相存储：增加集成测试与初始化文档`
  - `#16 [Tracking] 实现 Binance USDⓈ-M 运行时与配额安全恢复`
    - `#47 Binance 运行时：增加 USDⓈ-M 配置与客户端启动入口`
    - `#48 Binance 运行时：接通公共流、私有流与执行路径`
    - `#49 Binance 运行时：实现配额安全的恢复退避策略`
    - `#50 Binance 运行时：增加冒烟与恢复一致性测试`
  - `#17 [Tracking] 实现 OKX USDT 永续运行时与张数换算`
    - `#51 OKX 运行时：增加 USDT 永续配置与客户端启动入口`
    - `#52 OKX 运行时：实现张数到 base_qty 的换算`
    - `#53 OKX 运行时：强制单向持仓、逐仓与下单路径约束`
    - `#54 OKX 运行时：增加启动与换算回归测试`

### 第 3 阶段

- `#4 [Epic] 第 3 阶段：校验器与干跑演练`
  - `#18 [Tracking] 增加 Cryptofeed 校验器与偏差策略`
    - `#55 Cryptofeed 校验器：初始化服务与配置`
    - `#56 Cryptofeed 校验器：接入并归一化 Bybit、Binance、OKX 顶档行情`
    - `#57 Cryptofeed 校验器：实现新鲜度与顶档偏差策略`
    - `#58 Cryptofeed 校验器：产出 Supervisor 可消费的信号并补充测试`
  - `#19 [Tracking] 构建恢复场景故障注入工具`
    - `#59 故障注入：增加 WebSocket 断连注入器`
    - `#60 故障注入：增加私有流静默注入器`
    - `#61 故障注入：增加对账差异注入器`
    - `#62 故障注入：文档化操作员使用方式并接入运行手册`
  - `#20 [Tracking] 执行 BTC 与 ETH 的小规模干跑`
    - `#63 干跑演练：准备 BTC 与 ETH 的配置和安全闸门`
    - `#64 干跑演练：实现操作员清单与审计采集工具`
    - `#65 干跑演练：执行分阶段 BTC 与 ETH 演练并收集证据`
    - `#66 干跑演练：输出结项报告与发现总结`

### 第 4 阶段

- `#5 [Epic] 第 4 阶段：平台化`
  - `#21 [Tracking] 设计外部控制平面与操作员 API`
    - `#67 控制平面设计：定义外部 API 表面`
    - `#68 控制平面设计：定义操作员动作模型与权限边界`
    - `#69 控制平面设计：定义可交易性与恢复读模型`
    - `#70 控制平面设计：发布平台化切分边界与迁移计划`
  - `#84 [Tracking] 定义审计事件与操作员留痕边界`
    - `#85 审计设计：定义操作员动作与恢复事件模型`
    - `#86 审计设计：定义审计存储与查询边界`
    - `#87 审计设计：定义保留、脱敏与访问控制约束`
    - `#88 审计设计：补充运行手册与验收清单`

### 第 5 阶段

- `#6 [Epic] 第 5 阶段：Tier-1 原生适配器`
  - `#22 [Tracking] 设计 Tier-1 原生适配器接口与替换策略`
    - `#71 原生适配器策略：定义适配器接口与安全不变量`
    - `#72 原生适配器策略：规划 Tier-1 替换顺序`
    - `#73 原生适配器策略：定义影子验证与一致性校验`
    - `#74 原生适配器策略：定义回滚与回退规则`

### 第 6 阶段

- `#7 [Epic] 第 6 阶段：扩展与高可用`
  - `#23 [Tracking] 定义高可用与多账户扩展策略`
    - `#75 高可用与多账户策略：定义租户与账户模型`
    - `#76 高可用与多账户策略：定义高可用拓扑与故障切换职责`
    - `#77 高可用与多账户策略：定义长尾交易所准入清单`
    - `#78 高可用与多账户策略：定义运维成熟度里程碑与运行手册`
