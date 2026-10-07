from __future__ import annotations

from typing import Any

from src.shared.infrastructure.cosmos import CosmosService

from ..settings import DashboardRuntimeSettings


class DashboardSnapshotRepository:
    def __init__(
        self,
        cosmos_service: CosmosService,
        settings: DashboardRuntimeSettings,
    ) -> None:
        self._cosmos_service = cosmos_service
        self._settings = settings

    def get_latest_snapshot(self) -> dict[str, Any] | None:
        query = """
        SELECT VALUE {
            'timestamp': c.timestamp,
            'components': c.components
        }
        FROM c
        WHERE c.id = @id
        """

        snapshot = self._cosmos_service.query_items(
            container_name=self._settings.snapshot_container_name,
            query=query,
            parameters=[{'name': '@id', 'value': self._settings.snapshot_document_id}],
        )

        return next(iter(snapshot), None)

    def get_latest_update(self) -> dict | None:
        query = """
        SELECT VALUE c.components.time
        FROM c
        WHERE c.id = @id
        AND c.partition_key = @partition_key
        """

        latest_update = self._cosmos_service.query_items(
            container_name=self._settings.snapshot_container_name,
            query=query,
            parameters=[
                {'name': '@id', 'value': self._settings.snapshot_document_id},
                {'name': '@partition_key', 'value': self._settings.snapshot_partition_key},
            ],
        )

        return next(iter(latest_update), None)
