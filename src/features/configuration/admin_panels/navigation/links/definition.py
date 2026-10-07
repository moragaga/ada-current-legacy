from __future__ import annotations

from src.features.admin_framework.models import (
    AdminArtifactDefinition,
    AdminArtifactProjectionDefinition,
    AdminDefinition,
    AdminRemoteDefinition,
)
from src.features.configuration.models import FieldOption

from .row_factory_service import NavigationLinkRowFactoryService
from .schema import build_navigation_links_admin_schema

DEFAULT_PARENT_GROUP_OPTIONS: tuple[FieldOption, ...] = (
    FieldOption(
        label='Sin grupo',
        value='',
    ),
)


def build_navigation_links_admin_definition(
    *,
    parent_group_options: tuple[FieldOption, ...],
) -> AdminDefinition:
    schema = build_navigation_links_admin_schema(
        parent_group_options=parent_group_options,
    )

    return AdminDefinition(
        key='navigation_links',
        title='Administración de links de navegación',
        schema=schema,
        remote=AdminRemoteDefinition(
            sharepoint_filename='navigation_links.json.gz',
            relative_path='navigation',
        ),
        artifact=AdminArtifactDefinition(
            artifact_key='navigation_links',
            display_name='Links de navegación',
            category='navigation',
            content_type='application/json+gzip',
            schema_key=schema.key,
            projection=AdminArtifactProjectionDefinition(
                container_name='navigation_configuration',
                document_id='navigation_links',
                partition_key='navigation_links',
            ),
        ),
        row_id_field='link_id',
        row_factory=NavigationLinkRowFactoryService.build_new_row,
    )


NAVIGATION_LINKS_ADMIN_DEFINITION = build_navigation_links_admin_definition(
    parent_group_options=DEFAULT_PARENT_GROUP_OPTIONS,
)
