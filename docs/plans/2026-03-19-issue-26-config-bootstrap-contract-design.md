# #26 perp-platform 配置初始化契约设计

## 背景

`#26` 依赖 `#25` 已建立的 `perp_platform` 包和入口点，目标是在不引入交易所 runtime 细节的前提下，定义应用最小配置初始化契约。

本 issue 只解决 “应用启动时如何拿到一个合法配置对象”，不扩展到配置文件格式、外部秘钥加载或具体 venue 参数模型。

## 目标

- 定义最小配置对象 `AppConfig`
- 提供 `load_config(environ: Mapping[str, str] | None = None) -> AppConfig`
- 让 `cli.main()` 通过该契约完成最小启动
- 对非法配置给出清晰失败

## 非目标

- 不设计 TOML / YAML / JSON 配置文件格式
- 不引入第三方 settings 库
- 不建模交易所、账户、instrument 或 runtime 级配置
- 不实现共享测试基座

## 方案比较

### 方案 A：`dataclass` + 环境变量加载

- 优点：
  - 依赖最少
  - 初始化入口清晰
  - 不会过早冻结配置存储格式
- 缺点：
  - 未来若接文件配置，需要再扩一层入口

### 方案 B：`dataclass` + 文件加载

- 优点：
  - 更接近未来部署配置
- 缺点：
  - 过早把 issue 扩展成配置系统设计

### 方案 C：第三方 settings 框架

- 缺点：
  - 当前明显超配
  - 额外引入依赖和框架耦合

## 选型

采用方案 A：标准库 `dataclass` + 环境变量加载。

## 设计

### 配置对象

`AppConfig` 仅包含：

- `app_name`
- `environment`
- `log_level`

默认值：

- `app_name = "perp-platform"`
- `environment = "dev"`
- `log_level = "INFO"`

### 配置来源

通过环境变量加载：

- `PERP_PLATFORM_APP_NAME`
- `PERP_PLATFORM_ENVIRONMENT`
- `PERP_PLATFORM_LOG_LEVEL`

### 约束

- `environment` 只允许：
  - `dev`
  - `test`
  - `prod`
- `log_level` 只允许：
  - `DEBUG`
  - `INFO`
  - `WARNING`
  - `ERROR`

### CLI 集成

- `cli.main()` 启动时调用 `load_config()`
- 成功时输出包含 `app_name` 和 `environment` 的稳定 bootstrap 文案
- 非法配置直接抛出 `ValueError`

## 测试策略

采用 TDD：

1. 先写默认配置加载测试
2. 再写非法 `environment` / `log_level` 测试
3. 再写 CLI 通过配置契约完成启动的测试
4. 只实现使测试通过的最小代码

## 风险与控制

- 风险：把配置契约扩展成完整配置系统
  - 控制：字段限制在 3 个，只支持环境变量入口
- 风险：CLI 对配置耦合过深
  - 控制：`main()` 只负责调用 `load_config()` 并输出最小启动信息

## 验证

- `py -m pytest tests/perp_platform/test_config.py -q`
- `py -m pytest tests/perp_platform/test_entrypoint.py -q`
- `py -m pytest tests -q`
