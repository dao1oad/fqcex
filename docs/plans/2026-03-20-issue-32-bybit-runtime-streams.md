# Issue 32 Bybit Runtime Streams Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 为 Bybit runtime 补齐公共流、私有流与执行客户端的最小 wiring 对象，并把它们挂到 bootstrap 结果中。

**Architecture:** 在 `clients.py` 中定义可测试的客户端描述对象，在 `runtime.py` 中做轻量 wiring，然后由 `bootstrap.py` 统一返回。整个实现只处理配置与对象组装，不建立真实连接。

**Tech Stack:** Python 3.12、dataclasses、pytest

---

### Task 1: Add failing runtime wiring tests

**Files:**
- Create: `tests/perp_platform/test_bybit_runtime_clients.py`
- Modify: `tests/perp_platform/test_bybit_runtime_bootstrap.py`

**Step 1: Write the failing tests**

- 为 `wire_bybit_runtime()` 写测试，覆盖：
  - 无 API 凭证时没有 `private_stream`
  - 有 API 凭证时存在 `private_stream`
  - `execution_client` 继承 `rest_base_url`、`category`、`settle_coin`
- 为 `bootstrap_bybit_runtime()` 写测试，验证返回的 `runtime.public_stream` 与 `runtime.execution_client`

**Step 2: Run targeted tests to verify failure**

Run:

```bash
py -m pytest tests/perp_platform/test_bybit_runtime_clients.py tests/perp_platform/test_bybit_runtime_bootstrap.py -q
```

Expected:
- FAIL，因为 `clients.py` / `runtime.py` 及新的 bootstrap 字段尚不存在

**Step 3: Commit**

```bash
git add tests/perp_platform/test_bybit_runtime_clients.py tests/perp_platform/test_bybit_runtime_bootstrap.py
git commit -m "test: define bybit runtime wiring contract"
```

### Task 2: Implement Bybit client descriptors

**Files:**
- Create: `src/perp_platform/runtime/bybit/clients.py`
- Test: `tests/perp_platform/test_bybit_runtime_clients.py`

**Step 1: Write minimal implementation**

- 新增：
  - `BybitStreamClient`
  - `BybitExecutionClient`

**Step 2: Run targeted tests**

Run:

```bash
py -m pytest tests/perp_platform/test_bybit_runtime_clients.py -q
```

Expected:
- 仍然部分失败，因为 wiring 层尚未实现

**Step 3: Commit**

```bash
git add src/perp_platform/runtime/bybit/clients.py tests/perp_platform/test_bybit_runtime_clients.py
git commit -m "feat: add bybit runtime client descriptors"
```

### Task 3: Implement runtime wiring

**Files:**
- Create: `src/perp_platform/runtime/bybit/runtime.py`
- Modify: `src/perp_platform/runtime/bybit/__init__.py`
- Test: `tests/perp_platform/test_bybit_runtime_clients.py`

**Step 1: Write minimal implementation**

- 新增 `BybitRuntimeWiring`
- 新增 `wire_bybit_runtime(config)`
- 在 `__init__.py` 中导出 wiring 与 client descriptor

**Step 2: Run targeted tests**

Run:

```bash
py -m pytest tests/perp_platform/test_bybit_runtime_clients.py -q
```

Expected:
- PASS

**Step 3: Commit**

```bash
git add src/perp_platform/runtime/bybit/runtime.py src/perp_platform/runtime/bybit/__init__.py tests/perp_platform/test_bybit_runtime_clients.py
git commit -m "feat: wire bybit runtime clients"
```

### Task 4: Extend bootstrap result with runtime wiring

**Files:**
- Modify: `src/perp_platform/runtime/bybit/bootstrap.py`
- Test: `tests/perp_platform/test_bybit_runtime_bootstrap.py`

**Step 1: Update implementation**

- `BybitRuntimeBootstrapResult` 增加 `runtime`
- `bootstrap_bybit_runtime()` 调用 `wire_bybit_runtime()`
- 保持 `client_label` 与 `private_client_enabled` 现有行为

**Step 2: Run bootstrap tests**

Run:

```bash
py -m pytest tests/perp_platform/test_bybit_runtime_bootstrap.py -q
```

Expected:
- PASS

**Step 3: Commit**

```bash
git add src/perp_platform/runtime/bybit/bootstrap.py tests/perp_platform/test_bybit_runtime_bootstrap.py
git commit -m "feat: expose bybit runtime wiring from bootstrap"
```

### Task 5: Verify issue scope and prepare cloud handoff

**Files:**
- Modify: `docs/plans/2026-03-20-issue-32-bybit-runtime-streams-design.md`
- Modify: `docs/plans/2026-03-20-issue-32-bybit-runtime-streams.md`

**Step 1: Run verification**

Run:

```bash
py -m pytest tests/perp_platform/test_bybit_runtime_clients.py tests/perp_platform/test_bybit_runtime_bootstrap.py -q
py -m pytest tests/perp_platform -q
py -m pytest tests -q
```

Expected:
- 全部 PASS

**Step 2: Confirm scope**

- 仅存在 Bybit runtime wiring 相关文件改动
- 未引入真实 IO
- 未提前实现 `#33`

**Step 3: Commit**

```bash
git add docs/plans/2026-03-20-issue-32-bybit-runtime-streams-design.md docs/plans/2026-03-20-issue-32-bybit-runtime-streams.md
git commit -m "docs: add issue 32 bybit runtime wiring plan"
```
