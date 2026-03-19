# Issue #93 主 Agent / Orchestrator 云端执行模式设计

## 上下文

Issue `#93` 只负责把当前 issue orchestrator 从“强依赖本地 `.codex/orchestrator/*.json` 持久状态”收口到“GitHub / cloud task 可恢复”的最小运行模式，不改 `#32+` 业务能力，不引入长期驻留服务，也不绕过既有 issue 治理。

当前 orchestrator 已具备：

- `approval create/show/check`
- `gh sync`
- `next`
- `claim`
- `prepare`
- `start`
- `accept`
- `block`
- `close`

但它仍有两个 cloud 切换缺口：

1. `start/prepare` 产出的 dispatch pack 不足以脱离本地 `state.json` 独立完成 acceptance
2. `start` 默认写入本地 state，runbook 也没有给出 portable cloud mode 的最小操作路径

## 约束

- 只修改 `scripts/issue_orchestrator.py`、`src/perp_platform/orchestrator/`、`docs/runbooks/issue-orchestrator.md`、`tests/orchestrator/`、`tests/governance/` 与本 issue 的计划文档
- 不改 `.codex/` 本地状态文件内容
- 不实现 GitHub comment 驱动的全自动派发器
- 不扩展到多租户、多仓库或长期驻留 daemon

## 方案对比

### 方案 A：只写 runbook，不动代码

- 优点：改动最小
- 缺点：云端仍需要依赖当前本地 `state.json`，无法真正切换

### 方案 B：增加 portable dispatch / acceptance 包，并允许 `start` 跳过本地 state 持久化

- 优点：保留现有本地模式
- 优点：cloud task 可以只依赖 dispatch pack + review / changed-files 证据完成 acceptance
- 优点：改动范围仍然局限在 orchestrator 和测试
- 缺点：CLI 参数会略多一点

### 方案 C：把运行状态完全迁移到 GitHub issue comments

- 优点：最贴近云端驱动
- 缺点：超出本 issue 最小范围，且需要处理评论格式、回写冲突与状态恢复

## 推荐

采用 **方案 B**。

最小闭环是：

1. 让 `prepare` / `start` 生成可移植的 dispatch pack
2. dispatch pack 内显式携带 `claim_record` 与 `acceptance_payload`
3. `accept` 支持从 dispatch pack 而不是本地 `state.json` 完成校验
4. `start` 支持 `--skip-state-save` 和 `--dispatch-path`
5. runbook 明确本地模式与 cloud mode 的差异

## 设计

### 1. Portable Dispatch Pack

扩展 dispatch pack，新增两个结构：

- `claim_record`
  - issue / tracking / epic
  - approval bundle id
  - branch / worktree path
  - allowed / forbidden files
  - acceptance checks
- `acceptance_payload`
  - issue id
  - approval bundle id
  - allowed files
  - review required

这样 cloud task 拿到 dispatch pack 后，不依赖当前本机会话的 `state.json` 也能知道：

- 当前认领的是哪个 child issue
- 允许改哪些文件
- 返回哪些 acceptance 证据

### 2. CLI Cloud Mode

在 `prepare` 与 `start` 中新增：

- `--allowed-file`（可重复）
- `--forbidden-file`（可重复）
- `--acceptance-check`（可重复）
- `--dispatch-path`

在 `start` 中新增：

- `--skip-state-save`

行为定义：

- 本地模式：仍可保存 `state.json`
- cloud mode：`start --skip-state-save --dispatch-path ...` 只输出 portable dispatch pack，不写本地运行态

### 3. Acceptance Without Local State

扩展 `accept`：

- 保留现有 `--state-path` 路径，兼容本地模式
- 新增 `--dispatch-path`

当传入 `--dispatch-path` 时：

- 从 dispatch pack 读取 issue id 和 allowed files
- 校验 `changed_files`
- 校验 review evidence 非空
- 接受显式传入的 `head_sha`

这样 GitHub / cloud task 返回的结果只要附带：

- dispatch pack
- current head sha
- changed files
- review evidence

就能完成 acceptance。

### 4. Runbook

在 `docs/runbooks/issue-orchestrator.md` 增加 cloud mode 小节，明确：

- 本地模式继续使用 `.codex/orchestrator/state.json`
- cloud mode 使用 portable dispatch pack
- 推荐命令序列：
  1. `approval create`
  2. `gh sync`
  3. `start --skip-state-save --dispatch-path ...`
  4. cloud task 执行
  5. `accept --dispatch-path ...`

### 5. 测试

新增或更新测试，覆盖：

- `prepare` 输出 `claim_record` 和 `acceptance_payload`
- `prepare/start` 能接收允许文件、禁止文件和 acceptance checks
- `start --skip-state-save` 不写本地 state
- `accept --dispatch-path` 能在无 `state.json` 情况下完成 acceptance
- runbook 已记录 cloud mode 命令路径

## 验证

- `py -m pytest tests/orchestrator -q`
- `py -m pytest tests/governance/test_issue_orchestrator_runbook_contract.py -q`
- `py -m pytest tests -q`

## 超出范围

- Codex cloud UI / GitHub integration 的实际 dry run
- 长驻 orchestrator 服务
- 自动 merge / 自动 close / 自动派发 subagent
