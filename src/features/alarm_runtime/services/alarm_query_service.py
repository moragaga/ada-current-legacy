from __future__ import annotations

from typing import Any

from ..repositories.alarm_repository import AlarmRepository


class AlarmQueryService:
    def __init__(
        self,
        alarm_repository: AlarmRepository,
    ) -> None:
        self._alarm_repository = alarm_repository

    def get_active_alarms(self) -> dict[str, Any] | None:
        return self._alarm_repository.get_active_alarms()
