# Issue 70 Platform Boundary Implementation Plan

## Goal

补齐平台化切分边界与迁移顺序文档，并用契约测试锁定。

## Steps

1. 新增失败契约测试，要求：
   - `ARCHITECTURE.md` 有 Platformization Boundary 和 Migration Plan
   - `ROADMAP.md` 有 Phase 4 delivery order
2. 更新 `docs/architecture/ARCHITECTURE.md`
3. 更新 `docs/roadmap/ROADMAP.md`
4. 运行：
   - `py -m pytest tests/governance/test_platformization_boundary_contract.py -q`
   - `py -m pytest tests -q`
