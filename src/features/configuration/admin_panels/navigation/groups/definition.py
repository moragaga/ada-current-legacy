from __future__ import annotations

from src.features.admin_framework.models import (
    AdminArtifactDefinition,
    AdminArtifactProjectionDefinition,
    AdminDefinition,
    AdminRemoteDefinition,
)

from .row_factory_service import NavigationGroupRowFactoryService
from .schema import NAVIGATION_GROUPS_ADMIN_SCHEMA

NAVIGATION_GROUPS_ADMIN_DEFINITION = AdminDefinition(
    key='navigation_groups',
    title='Administración de grupos de navegación',
    schema=NAVIGATION_GROUPS_ADMIN_SCHEMA,
    remote=AdminRemoteDefinition(
        sharepoint_filename='navigation_groups.json.gz',
        relative_path='navigation',
    ),
    artifact=AdminArtifactDefinition(
        artifact_key='navigation_groups',
        display_name='Grupos de navegación',
        category='navigation',
        content_type='application/json+gzip',
        schema_key=NAVIGATION_GROUPS_ADMIN_SCHEMA.key,
        projection=AdminArtifactProjectionDefinition(
            container_name='navigation_configuration',
            document_id='navigation_groups',
            partition_key='navigation_groups',
        ),
    ),
    row_id_field='group_id',
    row_factory=NavigationGroupRowFactoryService.build_new_row,
)
