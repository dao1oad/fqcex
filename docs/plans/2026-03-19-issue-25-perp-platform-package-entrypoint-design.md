# #25 perp-platform Python 包与入口点设计

## 背景

`#25` 是 `#10 [Tracking] 搭建 perp-platform 应用骨架` 下的第一个 child issue。
当前主线还没有 `perp-platform` 的 Python 包、模块入口或最小启动链路，后续 `#26` 的配置初始化契约和 `#27` 的共享测试基座缺少稳定挂点。

根据 `docs/roadmap/ISSUE_HIERARCHY.md`，本 issue 只负责最小可导入、可执行、可测试的应用骨架，不承担配置系统和共享测试基础设施的职责。

## 目标

- 创建根级 Python 包 `perp_platform`
- 提供统一入口函数 `main(argv: list[str] | None = None) -> int`
- 支持 `python -m perp_platform` 启动
- 提供最小、稳定、可测试的 bootstrap 输出

## 非目标

- 不定义完整配置语义
- 不接入 `Supervisor`、`Cryptofeed` 或任意交易所 runtime
- 不实现共享测试 fixture 或复杂 CLI 参数体系
- 不引入额外第三方配置或 CLI 依赖

## 方案比较

### 方案 A：根级 Python 包

- 文件位于仓库根级 `pyproject.toml`、`src/perp_platform/`、`tests/perp_platform/`
- 优点：
  - 与当前根级 `pytest` 和 CI 入口最兼容
  - 能以最小改动建立稳定导入与执行链路
  - 给 `#26`、`#27` 提供明确挂点
- 缺点：
  - 暂时不使用现有 `apps/` 目录

### 方案 B：`apps/perp_platform` 子应用

- 更接近未来多应用布局
- 缺点：
  - 会把 `#25` 扩展到包发现、测试入口、CI 路径等非核心问题

### 方案 C：仅脚本入口

- 缺点：
  - 不符合 “创建 Python 包与入口点” 的 issue 目标
  - 后续仍需返工补正式包结构

## 选型

采用方案 A：根级 Python 包。

理由：`#25` 的核心是尽快建立最小闭环，而不是提前锁定未来 monorepo 目录策略。根级包能最稳妥地满足最小骨架需求，并降低对 `#26`、`#27` 的耦合。

## 设计

### 包结构

- `pyproject.toml`
- `src/perp_platform/__init__.py`
- `src/perp_platform/__main__.py`
- `src/perp_platform/cli.py`
- `tests/perp_platform/test_entrypoint.py`

### 行为契约

- `perp_platform.cli.main()` 是统一入口
- 不传入参数时输出稳定 bootstrap 文案并返回 `0`
- `python -m perp_platform` 复用同一入口逻辑
- 启动行为不依赖环境变量或外部服务

### 测试策略

采用 TDD：

1. 先写失败测试，验证 `main` 可导入
2. 再写失败测试，验证 `main([])` 返回 `0` 且输出稳定文案
3. 再写失败测试，验证 `python -m perp_platform` 可成功执行
4. 只实现让上述测试通过的最小代码

## 风险与控制

- 风险：过早引入配置或 runtime 细节，污染 `#25` 边界
  - 控制：测试仅验证导入、入口和最小输出
- 风险：包结构不利于后续扩展
  - 控制：入口集中在 `cli.py`，后续 `#26` 和 `#27` 可在不破坏入口契约的前提下扩展

## 验证

- `py -m pytest tests/perp_platform/test_entrypoint.py -q`
- `py -m pytest tests -q`
- `py -m perp_platform`
