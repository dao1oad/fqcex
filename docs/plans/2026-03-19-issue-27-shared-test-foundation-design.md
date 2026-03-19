# #27 perp-platform 共享测试基座设计

## 背景

`#25`、`#26` 已经建立了最小包入口和配置初始化契约，但现有测试里仍存在重复：

- 反复把当前 worktree 的 `src/` 注入到 `sys.path`
- 重复处理 `PERP_PLATFORM_*` 环境变量
- 直接在测试里散落 CLI 调用与输出捕获逻辑

`#27` 的目标是为后续 `#28+` 提供轻量、可复用的测试挂点，但不提前引入业务域 fixture。

## 目标

- 建立 `tests/perp_platform/support/` 共享测试支持包
- 建立顶层 `tests/conftest.py`
- 提供 `make_test_config(...)`
- 提供 `run_cli(...)`
- 提供环境变量隔离基础设施

## 非目标

- 不引入交易所 mock client
- 不引入数据库或网络 fixture
- 不建 Supervisor / runtime 专用 fixture
- 不重构现有业务逻辑

## 方案比较

### 方案 A：轻量 support 包 + 顶层 `conftest.py`

- 优点：
  - 只抽离当前已出现的重复
  - 适合作为后续 issue 的稳定测试挂点
  - 不会过早设计空壳目录树
- 缺点：
  - 当前内容较少，但这正是本 issue 的合理边界

### 方案 B：按领域预建大量 fixture 目录

- 缺点：
  - 当前没有对应业务对象，属于明显超前设计

### 方案 C：继续在各测试文件内联 helper

- 缺点：
  - 会继续复制 `sys.path`、环境变量和 CLI 调用逻辑

## 选型

采用方案 A：轻量 support 包 + 顶层 `conftest.py`。

## 设计

### 目录

- `tests/conftest.py`
- `tests/perp_platform/support/__init__.py`
- `tests/perp_platform/support/config.py`
- `tests/perp_platform/support/cli.py`
- `tests/perp_platform/test_support_contract.py`

### 共享能力

#### 环境隔离

- 在 `tests/conftest.py` 中增加自动 fixture
- 每个测试前清理：
  - `PERP_PLATFORM_APP_NAME`
  - `PERP_PLATFORM_ENVIRONMENT`
  - `PERP_PLATFORM_LOG_LEVEL`

#### 配置 helper

- `make_test_config(...)` 返回 `AppConfig`
- 默认值与当前配置契约一致
- 允许单个字段覆盖

#### CLI helper

- `run_cli(...)` 统一调用 `perp_platform.cli.main`
- 返回退出码和标准输出
- 内部负责把当前 worktree 的 `src/` 放到导入路径前面

### 测试迁移

- 现有 `test_config.py`、`test_entrypoint.py` 改为依赖 support helpers
- 新增 `test_support_contract.py` 验证 helper 自身契约

## 测试策略

采用 TDD：

1. 先写 support contract 测试
2. 再让现有入口与配置测试切到 support helpers
3. 最后只实现最小 helper 让测试通过

## 风险与控制

- 风险：把 support 层扩展成大型测试框架
  - 控制：只收敛当前重复，不新增业务域 fixture
- 风险：helper 掩盖真实行为
  - 控制：`run_cli()` 直接调用真实 `cli.main()`，`make_test_config()` 直接创建真实 `AppConfig`

## 验证

- `py -m pytest tests/perp_platform/test_support_contract.py -q`
- `py -m pytest tests/perp_platform -q`
- `py -m pytest tests -q`
