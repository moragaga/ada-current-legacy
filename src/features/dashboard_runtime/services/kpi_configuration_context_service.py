from __future__ import annotations

from ..models.kpi_configuration_definition import (
    KpiConfigurationDefinition,
    KpiConfigurationInformationDefinition,
)
from ..services.kpi_configuration_query_service import KpiConfigurationQueryService


class KpiConfigurationContextService:
    def __init__(
        self,
        kpi_configuration_query_service: KpiConfigurationQueryService,
    ) -> None:
        self._kpi_configuration_query_service = kpi_configuration_query_service

    def get_kpi_configuration_context(self) -> dict:
        build_definition = self._build_kpi_configuration_definition(
            configuration=self._kpi_configuration_query_service.get_kpi_configuration()
        )
        return build_definition

    def _build_kpi_configuration_definition(
        self, configuration: list[dict]
    ) -> KpiConfigurationDefinition:
        return KpiConfigurationDefinition(
            kpi_configuration=[
                self._map_row_kpi_configuration_definition(row) for row in configuration
            ]
        )

    def _map_row_kpi_configuration_definition(
        self, row: dict
    ) -> KpiConfigurationInformationDefinition:
        return KpiConfigurationInformationDefinition(
            kpi_name=str(row['kpi_name']).strip(),
            visualization=str(row['visualization']).strip().lower(),
            component=str(row['component']).strip().lower(),
            source=str(row['source']).strip().lower(),
            load_instant=self._to_bool(row.get('load_instant', True)),
            include_in_series_artifact=self._to_bool(row.get('include_in_series_artifact', False)),
        )

    @staticmethod
    def _to_bool(value: object) -> bool:
        if isinstance(value, bool):
            return value

        if value is None:
            return False

        return str(value).strip().lower() in {'true', '1', 'yes', 'si'}
