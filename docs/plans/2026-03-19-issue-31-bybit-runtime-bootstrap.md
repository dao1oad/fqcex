# Bybit Runtime Bootstrap Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add a minimal Bybit runtime config loader and bootstrap entrypoint without connecting to the network.

**Architecture:** Keep the feature isolated under `src/perp_platform/runtime/bybit/`, reusing the existing global `AppConfig` loader and exposing a stable bootstrap result object for future issues.

**Tech Stack:** Python 3.12, dataclasses, pytest

---

### Task 1: Lock the contract with tests

**Files:**
- Create: `tests/perp_platform/test_bybit_runtime_bootstrap.py`

1. Write failing tests for Bybit runtime config loading and bootstrap result shape.
2. Run `py -m pytest tests/perp_platform/test_bybit_runtime_bootstrap.py -q` and confirm failure.

### Task 2: Implement Bybit runtime config

**Files:**
- Create: `src/perp_platform/runtime/__init__.py`
- Create: `src/perp_platform/runtime/bybit/__init__.py`
- Create: `src/perp_platform/runtime/bybit/config.py`

1. Add `BybitRuntimeConfig`.
2. Load minimal env-driven fields with safe defaults and validation.
3. Re-run targeted tests.

### Task 3: Implement bootstrap entrypoint

**Files:**
- Create: `src/perp_platform/runtime/bybit/bootstrap.py`

1. Add stable bootstrap result object.
2. Compose global app config and Bybit runtime config.
3. Re-run targeted tests.

### Task 4: Verify the issue boundary

**Files:**
- Verify only the files above changed.

1. Run `py -m pytest tests/perp_platform -q`
2. Run `py -m pytest tests -q`
