# Backlog Review And Roadmap Alignment Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 让 `fqcex` 的 issue 树覆盖当前 roadmap 缺口，并给出一条可直接执行的后续开发顺序。

**Architecture:** 以 GitHub issue 树作为唯一执行入口。先补齐 Phase 1 的 worktree/CI/部署基座，再完成 `perp-platform` 骨架、统一模型和 Bybit 闭环；Phase 2、Phase 3 延续既有顺序；Phase 4 在控制平面之外单独补上审计留痕边界，然后再进入 Phase 5、Phase 6 的策略设计。

**Tech Stack:** GitHub Issues, `gh` CLI, Git worktrees, Python memory tooling, repo docs and runbooks.

---

### Task 1: 稳定 Phase 1 开发与交付基座

**Files:**
- Reference: `docs/roadmap/ISSUE_HIERARCHY.md`
- Reference: `docs/memory/ACTIVE_WORK.md`
- Issues: `#79`, `#80`, `#10`, `#25`, `#26`, `#27`, `#81`, `#82`, `#83`

**Step 1: 先修正 worktree 基线**

Run: `py -m pytest tests/memory -q`
Expected: 在新 worktree 中稳定复现并解决 `#80` 描述的分支名断言问题。

**Step 2: 建立最小应用骨架**

Run: `py -m pytest tests -q`
Expected: `#25-#27` 落地后，`perp-platform` 至少具备包入口、配置初始化契约和共享测试基座。

**Step 3: 收拢交付链路**

Run: `py -m pytest tests -q`
Expected: `#81-#83` 落地后，主线具备最小 CI、部署脚本、smoke 路径和 rollback runbook。

### Task 2: 完成 Phase 1 单交易所闭环

**Files:**
- Reference: `docs/roadmap/ISSUE_HIERARCHY.md`
- Issues: `#11`, `#28`, `#29`, `#30`, `#12`, `#31`, `#32`, `#33`, `#34`, `#13`, `#35`, `#36`, `#37`, `#38`

**Step 1: 先冻结统一模型**

Run: `py -m pytest tests -q`
Expected: `#28-#30` 先于所有交易所 runtime 细节落地。

**Step 2: 再完成 Bybit runtime 初始化**

Run: `py -m pytest tests/perp_platform/bybit -q`
Expected: `#31-#34` 让 Bybit 具备启动、接线、约束和基础冒烟能力。

**Step 3: 最后完成恢复与对账闭环**

Run: `py -m pytest tests/perp_platform/bybit -q`
Expected: `#35-#38` 让 Bybit 在回到 `LIVE` 前完成重连、对账与降级投影。

### Task 3: 完成 Phase 2 和 Phase 3 的多交易所基线与干跑前置

**Files:**
- Reference: `docs/roadmap/ISSUE_HIERARCHY.md`
- Issues: `#14-#20`, `#39-#66`

**Step 1: 按 Phase 2 顺序推进**

Run: `py -m pytest tests -q`
Expected: 先完成 `#39-#46` 的状态机与真相存储，再推进 `#47-#54` 的 Binance / OKX runtime。

**Step 2: 按 Phase 3 顺序推进**

Run: `py -m pytest tests -q`
Expected: 先完成 `#55-#62` 的校验器和故障注入，再执行 `#63-#66` 的干跑准备、证据采集和总结。

### Task 4: 完成 Phase 4 平台化并补齐审计留痕

**Files:**
- Reference: `docs/roadmap/ISSUE_HIERARCHY.md`
- Issues: `#21`, `#67`, `#68`, `#69`, `#70`, `#84`, `#85`, `#86`, `#87`, `#88`

**Step 1: 先完成控制平面动作与边界定义**

Run: `py -m pytest tests -q`
Expected: `#67-#70` 明确 API、动作模型、读模型和迁移切分线。

**Step 2: 再冻结 audit 边界**

Run: `py -m pytest tests -q`
Expected: `#85-#88` 单独补齐 roadmap 中已声明但原 issue 树缺失的 audit 事件、存储、安全和 runbook 约束。

### Task 5: 完成 Phase 5 到 Phase 6 的策略设计

**Files:**
- Reference: `docs/roadmap/ISSUE_HIERARCHY.md`
- Issues: `#22`, `#71`, `#72`, `#73`, `#74`, `#23`, `#75`, `#76`, `#77`, `#78`

**Step 1: 先冻结 Tier-1 原生适配器替换策略**

Run: `py -m pytest tests -q`
Expected: `#71-#74` 在不影响现有安全边界的前提下完成接口、替换顺序、影子验证和回滚规则设计。

**Step 2: 最后定义扩展与高可用策略**

Run: `py -m pytest tests -q`
Expected: `#75-#78` 基于前面阶段已冻结的控制平面和审计边界，补齐多账户、HA 和长尾准入规则。

### Task 6: 每轮完成后的固定校验

**Files:**
- Reference: `docs/memory/PROJECT_STATE.md`
- Reference: `docs/memory/ACTIVE_WORK.md`
- Reference: `docs/memory/SESSION_HANDOFF.md`

**Step 1: 刷新项目快照**

Run: `py scripts/update_project_memory.py`
Expected: `docs/memory/generated/project_snapshot.md` 反映当前分支、worktree、issues 和最近提交。

**Step 2: 补齐手工记忆入口**

Run: `git status --short --branch`
Expected: 任何影响 backlog、分支或运行安全判断的变化，都已同步回 memory 文档和相关 roadmap / runbook。
