# #56 Cryptofeed 顶档接入与归一化 Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 让 `checker` 能基于真实 `Cryptofeed` exchange 类接入 Bybit、BinanceFutures、OKX 的顶档行情，并归一化成统一模型。

**Architecture:** 使用 `Cryptofeed` 的 `TICKER` 通道作为三家统一顶档来源，在 checker 边界层预热 Phase 1 最小 symbol mapping，避免运行时做 REST 符号发现。归一化层从 `Ticker` 与 `Ticker.raw` 提取 bid/ask 与 size，输出仓库内部统一的 `CheckerTopOfBook`。

**Tech Stack:** Python 3.12, `cryptofeed`, `pytest`

---

### Task 1: Add failing tests for checker feed integration

**Files:**
- Create: `tests/perp_platform/test_checker_feeds.py`

**Step 1: Write the failing tests**

Add tests for:

- seeding Phase 1 symbol mappings
- building three feeds without REST symbol discovery
- normalizing Bybit / Binance / OKX ticker payloads
- rejecting missing size fields

**Step 2: Run tests to verify they fail**

Run: `py -m pytest tests/perp_platform/test_checker_feeds.py -q`

Expected: FAIL because `perp_platform.checker.models` and `perp_platform.checker.feeds` do not exist yet.

**Step 3: Commit**

```bash
git add tests/perp_platform/test_checker_feeds.py
git commit -m "test: add failing checker feed tests"
```

### Task 2: Add checker top-of-book model

**Files:**
- Create: `src/perp_platform/checker/models.py`
- Modify: `src/perp_platform/checker/__init__.py`

**Step 1: Write minimal implementation**

Add a frozen dataclass for normalized top-of-book with Decimal validation:

- `CheckerTopOfBook`
- `_to_decimal(...)` helper if needed

**Step 2: Run targeted tests**

Run: `py -m pytest tests/perp_platform/test_checker_feeds.py -q`

Expected: some tests still fail because feed integration is not implemented yet.

**Step 3: Commit**

```bash
git add src/perp_platform/checker/models.py src/perp_platform/checker/__init__.py
git commit -m "feat: add checker top-of-book model"
```

### Task 3: Implement symbol priming and feed builder

**Files:**
- Create: `src/perp_platform/checker/feeds.py`
- Modify: `pyproject.toml`

**Step 1: Implement Phase 1 symbol priming**

Add minimal mapping for:

- Bybit
- BinanceFutures
- OKX

Use `cryptofeed.symbols.Symbols.set(...)` to preload mappings for Phase 1 instruments.

**Step 2: Implement feed builder**

Add helpers for:

- importing `FeedHandler`, `TICKER`, `Bybit`, `BinanceFutures`, `OKX`
- building configured feed instances
- wiring a per-venue callback that normalizes `Ticker` events

**Step 3: Run targeted tests**

Run: `py -m pytest tests/perp_platform/test_checker_feeds.py -q`

Expected: normalization/build tests pass.

**Step 4: Commit**

```bash
git add pyproject.toml src/perp_platform/checker/feeds.py
git commit -m "feat: add checker cryptofeed feed builder"
```

### Task 4: Document checker top-of-book boundary

**Files:**
- Modify: `docs/architecture/ARCHITECTURE.md`

**Step 1: Update architecture doc**

Document:

- checker consumes `Cryptofeed TICKER`
- raw size fields stay at checker boundary
- normalized output is venue-neutral top-of-book

**Step 2: Run tests**

Run: `py -m pytest tests/perp_platform/test_checker_feeds.py -q`

Expected: PASS

**Step 3: Commit**

```bash
git add docs/architecture/ARCHITECTURE.md
git commit -m "docs: add checker top-of-book architecture note"
```

### Task 5: Run verification and prepare merge

**Files:**
- Verify only

**Step 1: Run checker-targeted tests**

Run: `py -m pytest tests/perp_platform/test_checker_feeds.py -q`

Expected: PASS

**Step 2: Run package tests**

Run: `py -m pytest tests/perp_platform -q`

Expected: PASS

**Step 3: Run full suite**

Run: `py -m pytest tests -q`

Expected: PASS

**Step 4: Reinstall editable package**

Run: `py -m pip install -e .`

Expected: PASS

**Step 5: Commit final integration**

```bash
git add pyproject.toml src/perp_platform/checker/__init__.py src/perp_platform/checker/models.py src/perp_platform/checker/feeds.py tests/perp_platform/test_checker_feeds.py docs/architecture/ARCHITECTURE.md docs/plans/2026-03-20-issue-56-checker-feeds-design.md docs/plans/2026-03-20-issue-56-checker-feeds.md
git commit -m "feat: add checker top-of-book feeds"
```
