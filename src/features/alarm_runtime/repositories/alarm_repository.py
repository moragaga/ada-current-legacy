from __future__ import annotations

from typing import Any

from src.shared.infrastructure.cosmos import CosmosService

from ..settings import AlarmRuntimeSettings


class AlarmRepository:
    def __init__(self, cosmos_service: CosmosService, settings: AlarmRuntimeSettings):
        self._cosmos_service = cosmos_service
        self._settings = settings

    def get_active_alarms(self) -> dict[str, Any] | None:
        query = """
        SELECT *
        FROM c
        WHERE c.id = @id
        """

        snapshot = self._cosmos_service.query_items(
            container_name=self._settings.alarm_container_name,
            query=query,
            parameters=[{'name': '@id', 'value': self._settings.alarm_document_id}],
        )

        return snapshot[0] if len(snapshot) > 0 else None
