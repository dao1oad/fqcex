from pathlib import Path


def test_issue_hierarchy_inserts_codex_cloud_migration_before_bybit_runtime_children() -> None:
    content = Path("docs/roadmap/ISSUE_HIERARCHY.md").read_text(encoding="utf-8")

    assert "#90 [Tracking] 迁移仓库到 Codex cloud 开发环境" in content
    assert "#95 Codex cloud 迁移：更新 issue hierarchy 与执行顺序" in content
    assert "#91 Codex cloud 迁移：标准化仓库 setup 与 Linux 兼容入口" in content
    assert "#92 Codex cloud 迁移：定义 environment、secrets 与网络访问约束" in content
    assert "#93 Codex cloud 迁移：调整主 agent / orchestrator 的云端执行模式" in content
    assert "#94 Codex cloud 迁移：完成 GitHub / Codex cloud dry run 与操作手册" in content

    assert content.index("#90 [Tracking] 迁移仓库到 Codex cloud 开发环境") < content.index(
        "#12 [Tracking] 实现 Bybit 线性永续运行时初始化"
    )
    assert (
        "#95 -> #91 -> #92 -> #93 -> #94 -> #32 -> #33 -> #34 -> #35 -> #36 -> #37 -> #38"
        in content
    )
