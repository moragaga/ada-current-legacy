from __future__ import annotations

from typing import Any

from src.shared.infrastructure.cosmos import CosmosService

from ..settings import KpiConfigurationRuntimeSettings


class KpiConfigurationRepository:
    def __init__(
        self,
        cosmos_service: CosmosService,
        settings: KpiConfigurationRuntimeSettings,
    ) -> None:
        self._cosmos_service = cosmos_service
        self._settings = settings

    def get_configuration(self) -> dict[str, Any] | None:
        query = """
        SELECT VALUE d
        FROM c
        JOIN d IN c.data
        WHERE c.id = @id
        """

        configuration = self._cosmos_service.query_items(
            container_name=self._settings.kpi_configuration_container_name,
            query=query,
            parameters=[{'name': '@id', 'value': self._settings.kpi_configuration_document_id}],
        )

        return configuration
