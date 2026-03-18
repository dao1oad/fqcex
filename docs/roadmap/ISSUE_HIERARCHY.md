# Issue 层级与执行规则

## 目标

本仓库的 backlog 固定采用三层结构：

- `Epic`
- `Tracking Parent Issue`
- `Child Implementation Issue`

后续任何编码、文档、集成、验证工作，都必须以 **child issue** 作为直接执行单元。

## 层级定义

### 1. Epic

职责：

- 表达 phase 目标
- 挂接 tracking parents
- 定义 phase 退出条件

规则：

- 使用标签 `type/epic`
- 不直接作为编码入口
- 只有在所有 tracking parents 完成后才关闭

### 2. Tracking Parent Issue

职责：

- 表达单个能力块的总边界
- 聚合 child issues
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
  - Objective
  - Ownership Boundary
  - Scope
  - Out of Scope
  - Dependencies
  - Expected Files
  - Deliverables
  - Acceptance Criteria
  - Verification
  - Close Rule

## 执行规则

- 只允许从 `type/task` issue 直接开始编码。
- 不允许直接从 `type/epic` 或 `type/tracking` issue 开始编码。
- 一个 subagent 一次只拥有一个 child issue。
- 如果执行中发现 scope 膨胀，必须新开 sibling child issue，而不是扩大原 issue 边界。
- 一个 PR 最好只对应一个 child issue；确有必要跨多个 child issue 时，必须在 PR 中说明。

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

### Phase 1

- `#2 [Epic] Phase 1 - Single Venue Loop`
  - `#10 [Tracking] Bootstrap perp-platform application skeleton`
    - `#25 Bootstrap perp-platform application skeleton: create Python package and entrypoint`
    - `#26 Bootstrap perp-platform application skeleton: add config bootstrap contract`
    - `#27 Bootstrap perp-platform application skeleton: add shared test harness`
  - `#11 [Tracking] Define canonical instrument and quantity model`
    - `#28 Canonical model: define instrument identity and market enums`
    - `#29 Canonical model: implement quantity normalization and OKX contract conversion`
    - `#30 Canonical model: document truth fields and architecture constraints`
  - `#12 [Tracking] Implement Bybit linear perpetual runtime bootstrap`
    - `#31 Bybit runtime bootstrap: add config and client bootstrap`
    - `#32 Bybit runtime bootstrap: wire public private and execution clients`
    - `#33 Bybit runtime bootstrap: enforce one-way isolated and order capability guards`
    - `#34 Bybit runtime bootstrap: add smoke tests for bootstrap and basic order path`
  - `#13 [Tracking] Implement Bybit recovery and reconciliation loop`
    - `#35 Bybit recovery loop: implement reconnect and resubscribe sequencing`
    - `#36 Bybit recovery loop: reconcile orders positions and balances before LIVE`
    - `#37 Bybit recovery loop: project REDUCE_ONLY and BLOCKED outcomes`
    - `#38 Bybit recovery loop: add recovery scenario tests and runbook notes`

### Phase 2

- `#3 [Epic] Phase 2 - Three Venue Baseline`
  - `#14 [Tracking] Implement supervisor tradeability state machine`
    - `#39 Supervisor state machine: define state enums and transition contract`
    - `#40 Supervisor state machine: implement stream trigger evaluation`
    - `#41 Supervisor state machine: project venue and symbol tradeability separately`
    - `#42 Supervisor state machine: add tests and architecture documentation`
  - `#15 [Tracking] Add PostgreSQL truth store schema`
    - `#43 PostgreSQL truth store: add core schema and migrations`
    - `#44 PostgreSQL truth store: implement repositories for orders positions and balances`
    - `#45 PostgreSQL truth store: implement tradeability and recovery persistence`
    - `#46 PostgreSQL truth store: add integration tests and bootstrap docs`
  - `#16 [Tracking] Implement Binance USDⓈ-M runtime and quota-safe recovery`
    - `#47 Binance runtime: add USDⓈ-M config and client bootstrap`
    - `#48 Binance runtime: wire public private and execution paths`
    - `#49 Binance runtime: implement quota-safe recovery backoff policy`
    - `#50 Binance runtime: add smoke and recovery consistency tests`
  - `#17 [Tracking] Implement OKX USDT swap runtime and contract conversion`
    - `#51 OKX runtime: add USDT swap config and client bootstrap`
    - `#52 OKX runtime: implement contract-size to base_qty conversion`
    - `#53 OKX runtime: enforce one-way isolated guards and order path`
    - `#54 OKX runtime: add smoke and conversion regression tests`

### Phase 3

- `#4 [Epic] Phase 3 - Checker and Dry Run`
  - `#18 [Tracking] Add Cryptofeed checker and divergence policies`
    - `#55 Cryptofeed checker: bootstrap service and configuration`
    - `#56 Cryptofeed checker: ingest and normalize top-of-book for Bybit Binance OKX`
    - `#57 Cryptofeed checker: implement freshness and divergence policies`
    - `#58 Cryptofeed checker: emit supervisor-ready signals and tests`
  - `#19 [Tracking] Build failure injection tooling for recovery scenarios`
    - `#59 Failure injection: add websocket disconnect injector`
    - `#60 Failure injection: add private-stream silence injector`
    - `#61 Failure injection: add reconcile-diff injector`
    - `#62 Failure injection: document operator usage and runbook integration`
  - `#20 [Tracking] Execute small-size dry run across BTC and ETH`
    - `#63 Dry run: prepare BTC and ETH configuration and safety gates`
    - `#64 Dry run: implement operator checklist and audit capture tooling`
    - `#65 Dry run: execute staged BTC and ETH rehearsal and collect evidence`
    - `#66 Dry run: publish findings and closeout report`

### Phase 4

- `#5 [Epic] Phase 4 - Platformization`
  - `#21 [Tracking] Design external control plane and operator APIs`
    - `#67 Control plane design: define external API surface`
    - `#68 Control plane design: define operator action command model and auth boundary`
    - `#69 Control plane design: define tradeability and recovery read models`
    - `#70 Control plane design: publish platformization cut line and migration plan`

### Phase 5

- `#6 [Epic] Phase 5 - Native Tier-1 Adapters`
  - `#22 [Tracking] Design Tier-1 native adapter interface and replacement strategy`
    - `#71 Native adapter strategy: define adapter interface and safety invariants`
    - `#72 Native adapter strategy: map Tier-1 replacement order`
    - `#73 Native adapter strategy: define shadow validation and parity checks`
    - `#74 Native adapter strategy: define rollback and fallback rules`

### Phase 6

- `#7 [Epic] Phase 6 - Scale and HA`
  - `#23 [Tracking] Define HA and multi-account expansion strategy`
    - `#75 HA and multi-account strategy: define tenancy and account model`
    - `#76 HA and multi-account strategy: define HA topology and failover responsibilities`
    - `#77 HA and multi-account strategy: define long-tail venue admission checklist`
    - `#78 HA and multi-account strategy: define operational maturity milestones and runbooks`
