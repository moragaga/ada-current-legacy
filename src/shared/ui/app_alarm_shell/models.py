from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AlarmShellDefinition:
    alarms_interval_ms: int
    show_alarms: bool = True
