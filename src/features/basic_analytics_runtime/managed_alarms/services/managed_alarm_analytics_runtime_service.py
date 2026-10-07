from __future__ import annotations

from typing import Any

from ..models.managed_alarm_counts import (
    ManagedAlarmAnalyticsCounts,
)
from ..repositories.managed_alarm_analytics_repository import (
    ManagedAlarmAnalyticsRepository,
)


class ManagedAlarmAnalyticsRuntimeService:
    def __init__(
        self,
        *,
        repository: ManagedAlarmAnalyticsRepository,
    ) -> None:
        self._repository = repository

    def get_snapshot(self) -> dict[str, Any]:
        return self._repository.get_snapshot()

    def get_counts(self) -> ManagedAlarmAnalyticsCounts:
        return self._repository.get_counts()

    def get_current_turn_management_count(self) -> int:
        return self.get_counts().current_turn_management_count


def get_managed_alarm_analytics_runtime_service() -> ManagedAlarmAnalyticsRuntimeService:
    return ManagedAlarmAnalyticsRuntimeService(
        repository=ManagedAlarmAnalyticsRepository(),
    )
