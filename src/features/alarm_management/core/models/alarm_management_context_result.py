from __future__ import annotations

from dataclasses import dataclass

from .alarm_management_context import AlarmManagementContext


@dataclass(frozen=True)
class AlarmManagementContextResult:
    status: str
    message: str | None = None
    context: AlarmManagementContext | None = None

    @property
    def is_ready(self) -> bool:
        return self.status == 'ready' and self.context is not None
