from __future__ import annotations

from typing import Any

from src.features.configuration.admin_panels.alarm_configuration.definition import (
    ALARM_CONFIGURATION_ADMIN_DEFINITION,
)

from .admin_rows_data_accessor import AdminRowsDataAccessor


class AlarmConfigurationRowsRepository:
    def __init__(
        self,
        *,
        data_accessor: AdminRowsDataAccessor | None = None,
    ) -> None:
        self._data_accessor = data_accessor or AdminRowsDataAccessor()

    def load_rows(self) -> list[dict[str, Any]]:
        return self._data_accessor.load_rows(
            definition=ALARM_CONFIGURATION_ADMIN_DEFINITION,
        )
