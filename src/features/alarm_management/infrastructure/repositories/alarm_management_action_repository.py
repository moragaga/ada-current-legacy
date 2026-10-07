from __future__ import annotations

from src.shared.infrastructure.cosmos import CosmosService

from ...core.models import AlarmManagementAction


class AlarmManagementActionRepository:
    def __init__(
        self,
        *,
        cosmos_service: CosmosService,
        container_name: str = 'alarm_management_actions',
    ) -> None:
        self._cosmos_service = cosmos_service
        self._container_name = container_name

    def save_action(
        self,
        *,
        action: AlarmManagementAction,
    ) -> bool:
        return self._cosmos_service.upsert(
            container_name=self._container_name,
            item=action.to_dict(),
        )
