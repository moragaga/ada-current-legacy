from __future__ import annotations

from src.features.admin_framework.models import (
    AdminArtifactDefinition,
    AdminArtifactProjectionDefinition,
    AdminDefinition,
    AdminRemoteDefinition,
)

from .schema import ALARM_CONFIGURATION_ADMIN_SCHEMA

ALARM_CONFIGURATION_ADMIN_DEFINITION = AdminDefinition(
    key='alarm_configuration',
    title='Administración de Alarmas',
    schema=ALARM_CONFIGURATION_ADMIN_SCHEMA,
    remote=AdminRemoteDefinition(
        sharepoint_filename='alarm_configuration.json.gz',
        relative_path='alarm',
    ),
    artifact=AdminArtifactDefinition(
        artifact_key='alarm_configuration',
        display_name='Configuración de Alarmas',
        category='alarmas',
        content_type='application/json+gzip',
        schema_key=ALARM_CONFIGURATION_ADMIN_SCHEMA.key,
        projection=AdminArtifactProjectionDefinition(
            container_name='alarm_configuration',
            document_id='alarm_configuration',
            partition_key='alarm_configuration',
        ),
    ),
    row_id_field='alarm_key',
)
