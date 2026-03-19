from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True)
class BybitStreamClient:
    channel: Literal["public", "private"]
    url: str
    category: str
    requires_auth: bool


@dataclass(frozen=True)
class BybitExecutionClient:
    rest_base_url: str
    category: str
    settle_coin: str
    api_key_present: bool
    api_secret_present: bool
