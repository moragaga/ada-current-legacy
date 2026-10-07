from __future__ import annotations

from typing import TypedDict


class AlarmRefreshLock(TypedDict):
    is_running: bool
    started_at: str | None
