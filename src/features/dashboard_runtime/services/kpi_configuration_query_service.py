from __future__ import annotations

from typing import Any

from ..repositories.kpi_configuration_repository import KpiConfigurationRepository


class KpiConfigurationQueryService:
    def __init__(
        self,
        kpi_configuration_repository: KpiConfigurationRepository,
    ) -> None:
        self._kpi_configuration_repository = kpi_configuration_repository

    def get_kpi_configuration(self) -> dict[str, Any] | None:
        return self._kpi_configuration_repository.get_configuration()
