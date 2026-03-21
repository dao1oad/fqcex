from __future__ import annotations

from pathlib import Path

from perp_platform.control_plane.actions import InMemoryOperatorActionAuditHook
from perp_platform.control_plane.live_safety import (
    FileBackedKillSwitch,
    LiveCanaryApproval,
    LiveCanaryRequest,
    LiveSafetyGate,
    LiveSafetyGateConfig,
)


def build_gate(tmp_path: Path, *, kill_switch_armed: bool = False) -> LiveSafetyGate:
    kill_switch_path = tmp_path / "kill-switch.flag"
    kill_switch_path.write_text(
        f"armed={'true' if kill_switch_armed else 'false'}\n",
        encoding="utf-8",
    )
    config = LiveSafetyGateConfig(
        max_notional_usd=250,
        allowed_venues=("BYBIT", "BINANCE", "OKX"),
        allowed_instruments=("BTC-USDT-PERP", "ETH-USDT-PERP"),
        kill_switch_path=kill_switch_path,
    )
    return LiveSafetyGate(
        config=config,
        kill_switch=FileBackedKillSwitch(kill_switch_path),
        audit_hook=InMemoryOperatorActionAuditHook(),
    )


def build_approval() -> LiveCanaryApproval:
    return LiveCanaryApproval(
        approved_by="alice",
        approved_at="2026-03-21T07:00:00Z",
        reason="approved live canary window",
    )


def test_live_safety_gate_rejects_missing_approval(tmp_path: Path) -> None:
    gate = build_gate(tmp_path)

    decision = gate.evaluate(
        LiveCanaryRequest(
            venue="BYBIT",
            instrument_id="BTC-USDT-PERP",
            requested_notional_usd=100,
            requested_by="bob",
            approval=None,
        )
    )

    assert decision.allowed is False
    assert decision.reason == "missing operator approval"
    assert decision.audit_event_id is None


def test_live_safety_gate_rejects_notional_above_limit(tmp_path: Path) -> None:
    gate = build_gate(tmp_path)

    decision = gate.evaluate(
        LiveCanaryRequest(
            venue="BYBIT",
            instrument_id="BTC-USDT-PERP",
            requested_notional_usd=500,
            requested_by="bob",
            approval=build_approval(),
        )
    )

    assert decision.allowed is False
    assert decision.reason == "requested notional exceeds live canary max"


def test_live_safety_gate_rejects_non_allowlist_target(tmp_path: Path) -> None:
    gate = build_gate(tmp_path)

    decision = gate.evaluate(
        LiveCanaryRequest(
            venue="DERIBIT",
            instrument_id="BTC-USDT-PERP",
            requested_notional_usd=100,
            requested_by="bob",
            approval=build_approval(),
        )
    )

    assert decision.allowed is False
    assert decision.reason == "venue is outside live canary allowlist"


def test_live_safety_gate_rejects_armed_kill_switch(tmp_path: Path) -> None:
    gate = build_gate(tmp_path, kill_switch_armed=True)

    decision = gate.evaluate(
        LiveCanaryRequest(
            venue="BYBIT",
            instrument_id="BTC-USDT-PERP",
            requested_notional_usd=100,
            requested_by="bob",
            approval=build_approval(),
        )
    )

    assert decision.allowed is False
    assert decision.reason == "kill switch is armed"


def test_live_safety_gate_allows_approved_request_and_records_audit(tmp_path: Path) -> None:
    gate = build_gate(tmp_path)

    decision = gate.evaluate(
        LiveCanaryRequest(
            venue="BYBIT",
            instrument_id="BTC-USDT-PERP",
            requested_notional_usd=100,
            requested_by="bob",
            approval=build_approval(),
        )
    )

    assert decision.allowed is True
    assert decision.reason == "live canary allowed"
    assert decision.audit_event_id == "audit-1"
