from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass(frozen=True)
class AlarmManagementRuntimeInputs:
    runtime_snapshot: dict[str, Any]
    alarm_configuration_rows: list[dict[str, Any]]
    message_configuration: dict[str, Any]
    managed_alarm_ids: set[str]
    now_utc: datetime
    shift_end_utc: datetime
