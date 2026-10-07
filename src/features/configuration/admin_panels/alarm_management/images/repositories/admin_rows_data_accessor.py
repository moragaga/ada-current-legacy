from __future__ import annotations

from typing import Any

from src.app.dependencies import (
    get_config_service,
    get_configuration_sharepoint_repository,
)
from src.features.admin_framework.models import AdminDefinition
from src.features.admin_framework.services import AdminDataService


class AdminRowsDataAccessor:
    def __init__(self) -> None:
        self._data_service = AdminDataService(
            repository=get_configuration_sharepoint_repository(),
            config_service=get_config_service(),
        )

    def load_rows(self, definition: AdminDefinition) -> list[dict[str, Any]]:
        rows = self._data_service.load(definition=definition)
        if rows is None:
            return []

        return [dict(row) for row in rows if isinstance(row, dict)]

    def save_rows(
        self,
        *,
        definition: AdminDefinition,
        rows: list[dict[str, Any]],
    ) -> None:
        self._data_service.save(definition=definition, rows=rows)
        return
