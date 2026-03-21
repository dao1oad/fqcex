# Issue 69 Read Models Implementation Plan

## Goal

补齐控制平面的最小读模型字段与数据来源映射，并用契约测试锁定。

## Steps

1. 新增失败契约测试，要求：
   - `control-plane-api.md` 定义 Venue/Instrument/Recovery 三种 read model
   - `DATA_MODEL.md` 写明与 `tradeability_states` / `recovery_runs` 的映射
   - 文档明确这些 read model 只是 projection
2. 更新 `docs/architecture/control-plane-api.md`
3. 更新 `docs/architecture/DATA_MODEL.md`
4. 运行：
   - `py -m pytest tests/governance/test_control_plane_read_models_contract.py -q`
   - `py -m pytest tests -q`
