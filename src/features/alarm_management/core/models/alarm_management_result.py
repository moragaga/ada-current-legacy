from __future__ import annotations

from dataclasses import dataclass

from .alarm_management_action import AlarmManagementAction


@dataclass(frozen=True)
class AlarmManagementResult:
    status: str
    message: str | None = None
    action: AlarmManagementAction | None = None

    @property
    def is_success(self) -> bool:
        return self.status == 'success'
