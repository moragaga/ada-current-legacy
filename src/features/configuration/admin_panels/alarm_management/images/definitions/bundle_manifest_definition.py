from __future__ import annotations

from src.features.admin_framework.models import (
    AdminArtifactDefinition,
    AdminArtifactProjectionDefinition,
    AdminDefinition,
    AdminRemoteDefinition,
)

from ..schemas.bundle_manifest_schema import (
    ALARM_IMAGE_BUNDLE_MANIFEST_ADMIN_SCHEMA,
)

ALARM_IMAGE_BUNDLE_MANIFEST_ADMIN_DEFINITION = AdminDefinition(
    key='alarm_image_bundle_manifest',
    title='Manifest Bundles Imágenes de Alarmas',
    schema=ALARM_IMAGE_BUNDLE_MANIFEST_ADMIN_SCHEMA,
    remote=AdminRemoteDefinition(
        sharepoint_filename='alarm_image_bundle_manifest.json.gz',
        relative_path='alarm',
    ),
    artifact=AdminArtifactDefinition(
        artifact_key='alarm_image_bundle_manifest',
        display_name='Manifest Bundles Imágenes de Alarmas',
        category='alarmas',
        content_type='application/json+gzip',
        schema_key=ALARM_IMAGE_BUNDLE_MANIFEST_ADMIN_SCHEMA.key,
        projection=AdminArtifactProjectionDefinition(
            container_name='alarm_configuration',
            document_id='alarm_image_bundle_manifest',
            partition_key='alarm_image_bundle_manifest',
        ),
    ),
    row_id_field='bundle_key',
)
