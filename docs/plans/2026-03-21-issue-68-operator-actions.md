# Issue 68 Operator Actions Implementation Plan

## Goal

为控制平面补齐最小 operator action 模型与权限边界文档，并用契约测试锁定。

## Steps

1. 新增失败契约测试，要求三份文档同时覆盖：
   - 只读 GET 和人工写动作的边界
   - `force_resume` 不能绕过恢复/对账前提
   - Codex cloud 不得持有控制平面写权限
2. 更新 `docs/architecture/control-plane-api.md`，补动作模型和权限边界
3. 更新 `docs/runbooks/force-resume-policy.md`，补最小审批和留痕规则
4. 更新 `SECURITY.md`，补控制平面写权限和 token 边界
5. 运行：
   - `py -m pytest tests/governance/test_operator_action_boundary_contract.py -q`
   - `py -m pytest tests -q`
