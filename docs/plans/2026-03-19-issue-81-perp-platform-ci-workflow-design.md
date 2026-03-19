# #81 perp-platform CI Workflow 设计

## 背景

当前仓库已经具备：

- `#25` 建立的最小 Python 包与入口点
- `#26` 建立的配置初始化契约
- `#27` 建立的共享测试基座
- `#89` 冻结的 required checks 名称：`governance-check`、`python-check`

但主线的 [`.github/workflows/ci.yml`](D:/fqcex/.worktrees/issue-81-perp-platform-ci-workflow/.github/workflows/ci.yml) 目前只有 `governance-check`，还没有任何面向 `perp_platform` 包安装与测试的 CI 护栏。`#81` 的目标是在不扩展到部署、Docker、lint 体系或 smoke 流程的前提下，补齐最小 Python CI。

## 目标

- 为 `perp_platform` 提供最小 CI 检查路径
- 保持现有 `governance-check` 不变
- 新增稳定的 `python-check` job
- 让仓库入口文档能说明当前最小 CI 护栏

## 非目标

- 不新增 CD 或生产部署
- 不引入 `ruff`、Playwright、Docker 或 smoke workflow
- 不修改 GitHub 平台侧 branch protection / ruleset
- 不硬编码仓库里不存在的 lint / smoke 命令

## 方案比较

### 方案 A：扩展现有 `ci.yml`

在现有 workflow 中保留 `governance-check`，新增 `python-check`。

优点：

- 改动最小
- 不会导致 required checks 来源漂移
- 与 `#89` 已冻结名称直接对齐

缺点：

- 单文件 workflow 会继续变长

### 方案 B：拆分为多个 workflow

将治理检查与 Python 检查拆成独立 workflow。

优点：

- 职责更清晰

缺点：

- 会同时改变 workflow 结构和 required checks 来源
- 对 `#81` 来说超出“最小 CI 护栏”边界

### 方案 C：一次纳入 lint / smoke / deploy

优点：

- 一次性更完整

缺点：

- 当前主线并不存在稳定的 lint / smoke / deploy 命令
- 会把 `#82` / `#83` 的范围偷渡进来

## 选型

采用方案 A。

理由：`#81` 的核心是以最小代价恢复主线对 `perp_platform` 的安装与测试验证，不是重构 CI 架构，也不是补齐完整交付流水线。

## 设计

### Workflow 结构

继续使用单个 [`.github/workflows/ci.yml`](D:/fqcex/.worktrees/issue-81-perp-platform-ci-workflow/.github/workflows/ci.yml)：

- `governance-check`
  - 名称保持不变
  - 继续验证治理基线文件存在
- `python-check`
  - `runs-on: ubuntu-latest`
  - `actions/checkout@v4`
  - `actions/setup-python@v5`
  - `python-version: "3.12"`
  - `python -m pip install --upgrade pip`
  - `python -m pip install -e .`
  - `python -m pytest tests -q`

### 触发条件

- `pull_request`
- `push` 到 `main`

不做 path filter。当前仓库规模很小，而且 `README`、治理文档、打包与测试之间有直接耦合，过早引入路径过滤容易漏检。

### README 更新

更新 [README.md](D:/fqcex/.worktrees/issue-81-perp-platform-ci-workflow/README.md)，补充一节最小 CI 说明：

- 当前 CI 包含 `governance-check` 和 `python-check`
- `python-check` 使用 Python `3.12`
- 安装方式是 `python -m pip install -e .`
- 测试命令是 `python -m pytest tests -q`
- Docker / smoke / deploy 留给后续 issue

### 测试策略

先写失败测试，验证稳定契约：

- workflow 中存在 `python-check`
- 使用 Python `3.12`
- 包含 `pip install -e .`
- 包含 `pytest tests -q`
- `README.md` 已说明 `governance-check` 和 `python-check`

测试只验证关键 token，不锁死完整 YAML / Markdown 文案。

## 风险与控制

- 风险：CI 改动超出 issue 边界
  - 控制：只新增最小 Python 安装与测试步骤，不引入 lint、Docker、smoke
- 风险：check 名称与 review 治理文档不一致
  - 控制：直接复用 `#89` 冻结的 `governance-check` / `python-check`
- 风险：CI 在干净环境里暴露 packaging 问题
  - 控制：这是 `#81` 应捕获的正常失败信号，不绕开 `pip install -e .`

## 验证

- `py -m pytest tests/governance/test_ci_workflow_contract.py -q`
- `py -m pytest tests -q`
- 人工检查 [`.github/workflows/ci.yml`](D:/fqcex/.worktrees/issue-81-perp-platform-ci-workflow/.github/workflows/ci.yml) 与 [README.md](D:/fqcex/.worktrees/issue-81-perp-platform-ci-workflow/README.md) 的 CI 说明一致
