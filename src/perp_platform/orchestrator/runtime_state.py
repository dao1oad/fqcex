"""Runtime state helpers for the issue orchestrator."""

import json
from dataclasses import asdict
from pathlib import Path

from .models import ApprovalBundle, OrchestratorState, WorkItem


def save_state(path: Path, work_item: WorkItem) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(asdict(work_item), indent=2), encoding="utf-8")


def load_state(path: Path) -> WorkItem:
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["status"] = OrchestratorState(payload["status"])
    payload["allowed_files"] = tuple(payload.get("allowed_files", ()))
    return WorkItem(**payload)


def save_approval_bundle(path: Path, approval_bundle: ApprovalBundle) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(asdict(approval_bundle), indent=2), encoding="utf-8")


def load_approval_bundle(path: Path) -> ApprovalBundle:
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["pause_only_on"] = tuple(payload["pause_only_on"])
    payload["recommended_defaults"] = tuple(payload["recommended_defaults"])
    return ApprovalBundle(**payload)


def save_dispatch_pack(path: Path, dispatch_pack: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(dispatch_pack, indent=2), encoding="utf-8")


def load_dispatch_pack(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))
