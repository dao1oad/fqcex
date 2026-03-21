from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path

from .actions import OperatorActionAuditHook, OperatorActionRequest


@dataclass(frozen=True)
class LiveSafetyGateConfig:
    max_notional_usd: Decimal
    allowed_venues: tuple[str, ...]
    allowed_instruments: tuple[str, ...]
    kill_switch_path: Path

    def __init__(
        self,
        *,
        max_notional_usd: Decimal | int | str,
        allowed_venues: tuple[str, ...],
        allowed_instruments: tuple[str, ...],
        kill_switch_path: Path,
    ) -> None:
        object.__setattr__(self, "max_notional_usd", Decimal(str(max_notional_usd)))
        object.__setattr__(self, "allowed_venues", allowed_venues)
        object.__setattr__(self, "allowed_instruments", allowed_instruments)
        object.__setattr__(self, "kill_switch_path", kill_switch_path)


@dataclass(frozen=True)
class LiveCanaryApproval:
    approved_by: str
    approved_at: str
    reason: str


@dataclass(frozen=True)
class LiveCanaryRequest:
    venue: str
    instrument_id: str
    requested_notional_usd: Decimal
    requested_by: str
    approval: LiveCanaryApproval | None

    def __init__(
        self,
        *,
        venue: str,
        instrument_id: str,
        requested_notional_usd: Decimal | int | str,
        requested_by: str,
        approval: LiveCanaryApproval | None,
    ) -> None:
        object.__setattr__(self, "venue", venue)
        object.__setattr__(self, "instrument_id", instrument_id)
        object.__setattr__(
            self, "requested_notional_usd", Decimal(str(requested_notional_usd))
        )
        object.__setattr__(self, "requested_by", requested_by)
        object.__setattr__(self, "approval", approval)


@dataclass(frozen=True)
class LiveCanaryDecision:
    allowed: bool
    reason: str
    audit_event_id: str | None = None


@dataclass(frozen=True)
class FileBackedKillSwitch:
    path: Path

    def is_armed(self) -> bool:
        if not self.path.exists():
            return True

        for raw_line in self.path.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            key, separator, value = line.partition("=")
            if separator and key.strip() == "armed":
                return value.strip().lower() == "true"
        return False


@dataclass
class LiveSafetyGate:
    config: LiveSafetyGateConfig
    kill_switch: FileBackedKillSwitch
    audit_hook: OperatorActionAuditHook

    def evaluate(self, request: LiveCanaryRequest) -> LiveCanaryDecision:
        if request.approval is None:
            return LiveCanaryDecision(
                allowed=False,
                reason="missing operator approval",
            )

        if request.venue not in self.config.allowed_venues:
            return LiveCanaryDecision(
                allowed=False,
                reason="venue is outside live canary allowlist",
            )

        if request.instrument_id not in self.config.allowed_instruments:
            return LiveCanaryDecision(
                allowed=False,
                reason="instrument is outside live canary allowlist",
            )

        if request.requested_notional_usd > self.config.max_notional_usd:
            return LiveCanaryDecision(
                allowed=False,
                reason="requested notional exceeds live canary max",
            )

        if self.kill_switch.is_armed():
            return LiveCanaryDecision(
                allowed=False,
                reason="kill switch is armed",
            )

        audit_event_id = self.audit_hook.record(
            OperatorActionRequest(
                action_type="approve_live_canary",
                target_scope={
                    "venue": request.venue,
                    "instrument_id": request.instrument_id,
                    "requested_notional_usd": str(request.requested_notional_usd),
                    "requested_by": request.requested_by,
                },
                requested_by=request.approval.approved_by,
                reason=request.approval.reason,
                requested_at=request.approval.approved_at,
            )
        )
        return LiveCanaryDecision(
            allowed=True,
            reason="live canary allowed",
            audit_event_id=audit_event_id,
        )
