from __future__ import annotations

from flask import session

from src.app.dependencies import (
    get_app_runtime_profile,
    get_config_manifest_service,
    get_config_service,
    get_configuration_sharepoint_repository,
)
from src.features.admin_framework.callbacks import register_admin_callback
from src.features.admin_framework.services import AdminDataService

from .definition import build_kpi_configuration_admin_definition


def register_kpi_configuration_admin_callback() -> None:
    def _after_save(definition, normalized_rows: list[dict]) -> list[str]:
        updated_by = (session.get('identity') or {}).get('email')

        ok = get_config_manifest_service().register_update(
            definition=definition,
            rows=normalized_rows,
            updated_by=updated_by,
        )

        if not ok:
            return ['El archivo se guardó, pero no se pudo actualizar el config manifest.']

        return []

    register_admin_callback(
        definition_factory=lambda: build_kpi_configuration_admin_definition(
            app_runtime_profile=get_app_runtime_profile(),
        ),
        data_service_factory=lambda: AdminDataService(
            repository=get_configuration_sharepoint_repository(),
            config_service=get_config_service(),
        ),
        after_save=_after_save,
    )
