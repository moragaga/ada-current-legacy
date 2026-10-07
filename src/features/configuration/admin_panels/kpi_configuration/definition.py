from __future__ import annotations

from src.features.admin_framework.models import (
    AdminArtifactDefinition,
    AdminArtifactProjectionDefinition,
    AdminDefinition,
    AdminRemoteDefinition,
)
from src.features.configuration.services.config_app_runtime_profile import ConfigAppRuntimeProfile

from .schema import build_kpi_configuration_admin_schema


def build_kpi_configuration_admin_definition(
    *,
    app_runtime_profile: ConfigAppRuntimeProfile,
) -> AdminDefinition:
    components = app_runtime_profile.build_component_select_configuration()

    schema = build_kpi_configuration_admin_schema(
        components=components,
    )

    return AdminDefinition(
        key='kpi_configuration',
        title='Administración de KPI',
        schema=schema,
        remote=AdminRemoteDefinition(
            sharepoint_filename='kpi_configuration.json.gz',
            relative_path='kpi',
        ),
        artifact=AdminArtifactDefinition(
            artifact_key='kpi_configuration',
            display_name='Configuración de KPI',
            category='kpi',
            content_type='application/json+gzip',
            schema_key=schema.key,
            projection=AdminArtifactProjectionDefinition(
                container_name='kpi_configuration',
                document_id='kpi_configuration',
                partition_key='kpi_configuration',
            ),
        ),
        row_id_field='key',
    )
