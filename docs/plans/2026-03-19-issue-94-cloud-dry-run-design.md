# Issue #94 GitHub / Codex Cloud Dry Run 设计

## 上下文

Issue `#94` 是 Codex cloud 迁移的最后一跳。`#91` 已标准化 Linux/Bash setup，`#92` 已冻结 environment / secrets / 网络边界，`#93` 已给 orchestrator 增加 portable cloud mode。当前缺的不是代码能力，而是：

- 一个清晰的 GitHub -> Codex cloud 操作路径
- 可审计的 dry run 证据
- 面向后续 child issue 的 operator 手册

## 约束

- 只修改 `CONTRIBUTING.md`、`docs/runbooks/`、`.github/`、`tests/governance/` 与本 issue 的计划文档
- dry run 不接入真实交易凭证，不访问真实交易所 API
- 不引入生产 deploy 流水线
- 不扩展到 `#32+` 运行时业务实现

## 方案对比

### 方案 A：只写文档，不做真实 dry run

- 优点：最安全
- 缺点：不满足“至少一次可审计 dry run”的验收标准

### 方案 B：文档 + PR 模板 + 真实 GitHub PR 上的 Codex cloud dry run

- 优点：直接验证最小任务入口
- 优点：能沉淀具体的 operator 手册与证据记录
- 优点：不需要引入额外平台代码
- 缺点：依赖仓库已连接 Codex cloud / GitHub integration

### 方案 C：先接 GitHub Action 再做 dry run

- 优点：自动化更强
- 缺点：超出本 issue 的最小范围，也不是 Codex GitHub integration 的最短路径

## 推荐

采用 **方案 B**。

最小闭环是：

1. 更新 `CONTRIBUTING.md`，明确云端 issue 工作流
2. 更新 `.github/PULL_REQUEST_TEMPLATE.md`，加入 Codex cloud evidence 区段
3. 新增 `docs/runbooks/codex-cloud-dry-run.md`
4. 加一个治理契约测试，冻结这些入口
5. 基于 `#94` 分支创建 PR，发起一次真实 `@codex ...` dry run
6. 把 PR URL、触发 comment URL、Codex 响应 URL 和结果写回 runbook

## 设计

### 1. 仓库入口文档

`CONTRIBUTING.md` 新增 `Codex Cloud Workflow` 小节，约束：

- 迁移完成后的 child issue 默认走 PR + Codex cloud，不再默认本地 direct-to-main
- operator 先准备 branch / PR，再通过 GitHub comment 触发 Codex
- `@codex review` 用于 review
- 非 `review` 的 `@codex ...` comment 用于启动 cloud task
- dry run / issue 执行完成后必须回填 review evidence 和验证结果

### 2. PR 模板

在 `.github/PULL_REQUEST_TEMPLATE.md` 中新增 `Codex Cloud Evidence` 区段，至少包含：

- Dry Run PR URL
- Trigger Comment URL
- Codex Response URL
- Outcome

这样后续每个云端 issue 都有固定留痕位置。

### 3. Dry Run Runbook

新增 `docs/runbooks/codex-cloud-dry-run.md`，包含：

- 先决条件
  - Codex cloud environment 已配置
  - 仓库已接入 GitHub integration
  - `AGENTS.md` / setup / cloud security / orchestrator cloud mode 已存在
- 操作步骤
  1. 创建 issue 分支
  2. 推送并开 PR
  3. 在 PR comment 中使用 `@codex ...`
  4. 等待 Codex 响应
  5. 记录 comment / review URL
  6. 如失败则回退到本地或人工排障
- Dry Run Record
  - 日期
  - PR URL
  - Trigger Comment URL
  - Codex Response URL
  - Outcome

### 4. 治理测试

新增 `tests/governance/test_codex_cloud_dry_run_contract.py`，验证：

- `CONTRIBUTING.md` 已记录 cloud workflow 与 `@codex` 入口
- PR 模板已有 `Codex Cloud Evidence`
- runbook 已记录 dry run 操作步骤和 dry run record

### 5. 真实 Dry Run

使用 `#94` 的实际 PR 执行一次最小 cloud task：

- 触发 comment 采用非 `review` 的 `@codex ...` 指令
- 要求只总结和核对 runbook，不做代码改动
- 记录 Codex 的回复链接作为 dry run evidence

## 验证

- `py -m pytest tests/governance/test_codex_cloud_dry_run_contract.py -q`
- `py -m pytest tests/governance -q`
- dry run PR comment 与 Codex 响应人工核对

## 超出范围

- 真实交易或真实账户联调
- 长驻自动化服务
- 多仓库 Codex 管理
- `#32+` 业务实现本身
