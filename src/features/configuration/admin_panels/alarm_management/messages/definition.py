from __future__ import annotations

from src.features.admin_framework.models import (
    AdminArtifactDefinition,
    AdminArtifactProjectionDefinition,
    AdminDefinition,
    AdminRemoteDefinition,
)

from .constants import ALARM_MANAGEMENT_MESSAGES_ADMIN_KEY
from .schema import ALARM_MANAGEMENT_MESSAGE_ROW_SCHEMA

ALARM_MANAGEMENT_MESSAGES_ADMIN_DEFINITION = AdminDefinition(
    key=ALARM_MANAGEMENT_MESSAGES_ADMIN_KEY,
    title='Administración de mensajes de gestión de alarmas',
    schema=ALARM_MANAGEMENT_MESSAGE_ROW_SCHEMA,
    remote=AdminRemoteDefinition(
        sharepoint_filename='alarm_management_message_configuration.json.gz',
        relative_path='alarm',
    ),
    artifact=AdminArtifactDefinition(
        artifact_key='alarm_management_message_configuration',
        display_name='Mensajes de gestión de alarmas',
        category='alarmas',
        content_type='application/json+gzip',
        schema_key=ALARM_MANAGEMENT_MESSAGE_ROW_SCHEMA.key,
        projection=AdminArtifactProjectionDefinition(
            container_name='alarm_management_message_configuration',
            document_id='alarm_management_message_configuration',
            partition_key='alarm_management_message_configuration',
        ),
    ),
    row_id_field='message_code',
)
