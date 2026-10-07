from __future__ import annotations

from typing import Any

from src.features.configuration.models import AdminSchema, FieldDefinition


def build_kpi_configuration_admin_schema(
    *,
    components: dict[str, Any],
) -> AdminSchema:
    return AdminSchema(
        key='kpi_configuration',
        title='Administración configuración de KPI',
        fields=(
            FieldDefinition(
                name='kpi_name',
                label='Nombre del KPI',
                field_type='text',
                required=True,
            ),
            FieldDefinition(
                name='component',
                label='Componente',
                field_type='select',
                required=True,
                **components,
            ),
            FieldDefinition(
                name='include_latest',
                label='Kpi Instantáneo',
                field_type='boolean',
                required=True,
                default_value=True,
            ),
            FieldDefinition(
                name='include_timeseries',
                label='Serie de Tiempo',
                field_type='boolean',
                required=True,
                default_value=False,
            ),
        ),
    )
