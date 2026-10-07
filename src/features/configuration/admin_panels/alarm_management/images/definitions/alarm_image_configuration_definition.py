from __future__ import annotations

from src.features.admin_framework.models import (
    AdminArtifactDefinition,
    AdminArtifactProjectionDefinition,
    AdminDefinition,
    AdminRemoteDefinition,
)

from ..schemas.alarm_image_configuration_schema import (
    ALARM_IMAGE_CONFIGURATION_ADMIN_SCHEMA,
)

ALARM_IMAGE_CONFIGURATION_ADMIN_DEFINITION = AdminDefinition(
    key='alarm_image_configuration',
    title='Administración Imágenes de Alarmas',
    schema=ALARM_IMAGE_CONFIGURATION_ADMIN_SCHEMA,
    remote=AdminRemoteDefinition(
        sharepoint_filename='alarm_image_configuration.json.gz',
        relative_path='alarm',
    ),
    artifact=AdminArtifactDefinition(
        artifact_key='alarm_image_configuration',
        display_name='Configuración de Imágenes de Alarmas',
        category='alarmas',
        content_type='application/json+gzip',
        schema_key=ALARM_IMAGE_CONFIGURATION_ADMIN_SCHEMA.key,
        projection=AdminArtifactProjectionDefinition(
            container_name='alarm_configuration',
            document_id='alarm_image_configuration',
            partition_key='alarm_image_configuration',
        ),
    ),
    row_id_field='image_key',
)
