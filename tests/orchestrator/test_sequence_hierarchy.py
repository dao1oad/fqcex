from perp_platform.orchestrator.sequence import parse_issue_hierarchy


def test_parse_issue_hierarchy_extracts_child_order() -> None:
    content = """
- `#2 [Epic] 第 1 阶段：单交易所闭环`
  - `#11 [Tracking] 定义统一合约与数量模型`
    - `#28 统一模型：定义合约标识与市场枚举`
    - `#29 统一模型：实现数量归一化与 OKX 张数换算`
    - `#30 统一模型：文档化真相字段与架构约束`
"""

    hierarchy = parse_issue_hierarchy(content)

    assert hierarchy[30]["tracking_issue_id"] == 11
    assert hierarchy[30]["epic_issue_id"] == 2
    assert hierarchy[30]["sequence_index"] == 2


def test_parse_issue_hierarchy_keeps_global_child_order_across_trackings() -> None:
    content = """
- `#2 [Epic] 第 1 阶段：单交易所闭环`
  - `#11 [Tracking] 定义统一合约与数量模型`
    - `#28 统一模型：定义合约标识与市场枚举`
    - `#29 统一模型：实现数量归一化与 OKX 张数换算`
    - `#30 统一模型：文档化真相字段与架构约束`
  - `#12 [Tracking] 实现 Bybit 线性永续运行时初始化`
    - `#31 Bybit 运行时初始化：增加配置与客户端启动入口`
"""

    hierarchy = parse_issue_hierarchy(content)

    assert hierarchy[30]["sequence_index"] == 2
    assert hierarchy[31]["sequence_index"] == 3
