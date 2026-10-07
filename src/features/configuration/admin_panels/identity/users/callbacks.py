from __future__ import annotations

from src.app.dependencies import (
    get_config_service,
    get_configuration_sharepoint_repository,
    get_identity_sync_service,
)
from src.features.admin_framework.callbacks import register_admin_callback
from src.features.admin_framework.services import AdminDataService

from .definition import IDENTITY_USERS_ADMIN_DEFINITION


def register_identity_users_admin_callback() -> None:
    def _after_save(_definition, _normalized_rows: list[dict]) -> list[str]:
        get_identity_sync_service().invalidate()
        return []

    register_admin_callback(
        definition_factory=lambda: IDENTITY_USERS_ADMIN_DEFINITION,
        data_service_factory=lambda: AdminDataService(
            repository=get_configuration_sharepoint_repository(),
            config_service=get_config_service(),
        ),
        after_save=_after_save,
    )
