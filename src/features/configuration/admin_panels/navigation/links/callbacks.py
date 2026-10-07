from __future__ import annotations

from flask import session

from src.app.dependencies import (
    get_config_manifest_service,
    get_config_service,
    get_configuration_sharepoint_repository,
    get_navigation_cache_service,
)
from src.features.admin_framework.callbacks import register_admin_callback
from src.features.admin_framework.services import AdminDataService

from .definition import build_navigation_links_admin_definition
from .group_options import build_navigation_group_options


def register_navigation_links_admin_callback() -> None:
    def _build_definition():
        group_rows = get_configuration_sharepoint_repository().load_rows(
            filename='navigation_groups.json.gz',
            relative_path='navigation',
        )

        return build_navigation_links_admin_definition(
            parent_group_options=build_navigation_group_options(group_rows),
        )

    def _after_save(definition, normalized_rows: list[dict]) -> list[str]:
        updated_by = (session.get('identity') or {}).get('email')

        ok = get_config_manifest_service().register_update(
            definition=definition,
            rows=normalized_rows,
            updated_by=updated_by,
        )

        if not ok:
            return ['El archivo se guardó, pero no se pudo actualizar el config manifest.']

        get_navigation_cache_service().invalidate()
        return []

    register_admin_callback(
        definition_factory=_build_definition,
        data_service_factory=lambda: AdminDataService(
            repository=get_configuration_sharepoint_repository(),
            config_service=get_config_service(),
        ),
        after_save=_after_save,
    )
