from __future__ import annotations

from flask import current_app

from src.features.alarm_management.core.services import (
    AlarmManagementUseCaseService,
)
from src.features.alarm_runtime.front_context.distributed import (
    DistributedAlarmContextService,
)
from src.features.configuration.admin_panels.alarm_management.messages.services import (
    AlarmMessageAdminService,
)
from src.features.configuration.admin_panels.publication_manager.services import (
    PublicationManagerActionService,
)

# # Activar cuando exista una app genérica usando alarm_monitor/panel.
# from src.features.alarm_runtime.front_context.generic import (
#     GenericAlarmContextService,
# )
from src.features.configuration.repositories import ConfigurationSharepointRepository
from src.features.configuration.services import (
    ConfigManifestService,
    ConfigService,
)
from src.features.configuration.services.config_app_runtime_profile import ConfigAppRuntimeProfile
from src.features.dashboard_runtime.services import DashboardContextService
from src.features.identity.services import IdentitySyncService
from src.features.navigation.services import NavigationCacheService
from src.features.user_sessions.services import UserSessionTrackingService
from src.shared.infrastructure.cosmos import CosmosService


def get_cosmos_service() -> CosmosService:
    service = current_app.extensions.get('cosmos_service')
    if service is None:
        raise RuntimeError('[ERROR] CosmosService is not registered in app.extensions')
    return service


def get_identity_sync_service() -> IdentitySyncService:
    service = current_app.extensions.get('identity_sync_service')
    if service is None:
        raise RuntimeError('[ERROR] IdentitySyncService is not registered in app.extensions')
    return service


def get_configuration_sharepoint_repository() -> ConfigurationSharepointRepository:
    service = current_app.extensions.get('configuration_sharepoint_repository')
    if service is None:
        raise RuntimeError('[ERROR] ConfigurationRepository is not registered in app.extensions')
    return service


def get_config_service() -> ConfigService:
    service = current_app.extensions.get('config_service')
    if service is None:
        raise RuntimeError('[ERROR] ConfigService is not registered in app.extensions')
    return service


def get_config_manifest_service() -> ConfigManifestService:
    service = current_app.extensions.get('config_manifest_service')
    if service is None:
        raise RuntimeError('[ERROR] ConfigManifestService is not registered in app.extensions')
    return service


def get_navigation_cache_service() -> NavigationCacheService:
    service = current_app.extensions.get('navigation_cache_service')
    if service is None:
        raise RuntimeError('[ERROR] NavigationCacheService is not registered in app.extensions')
    return service


def get_dashboard_context_service() -> DashboardContextService:
    service = current_app.extensions.get('dashboard_context_service')
    if service is None:
        raise RuntimeError('[ERROR] DashboardContextService is not registered in app.extensions')
    return service


def get_distributed_alarm_context_service() -> DistributedAlarmContextService:
    service = current_app.extensions.get(
        'distributed_alarm_context_service',
    )
    if service is None:
        raise RuntimeError('distributed_alarm_context_service has not been initialized.')
    return service


# Activar cuando exista una app genérica usando alarm_monitor/panel.
# def get_generic_alarm_context_service() -> GenericAlarmContextService:
#     service = current_app.extensions.get('generic_alarm_context_service')
#     if service is None:
#         raise RuntimeError(
#             'generic_alarm_context_service has not been initialized.'
#         )
#     return service


def get_publication_manager_action_service() -> PublicationManagerActionService:
    service = current_app.extensions.get('publication_manager_action_service')
    if service is None:
        raise RuntimeError(
            '[ERROR] PublicationManagerActionService is not registered in app.extensions'
        )
    return service


def get_alarm_message_admin_service() -> AlarmMessageAdminService:
    service = current_app.extensions.get('alarm_message_admin_service')
    if service is None:
        raise RuntimeError('[ERROR] AlarmMessageAdminService is not registered in app.extensions')
    return service


def get_alarm_management_use_case_service() -> AlarmManagementUseCaseService:
    service = current_app.extensions.get('alarm_management_use_case_service')
    if service is None:
        raise RuntimeError(
            '[ERROR] AlarmManagementUseCaseService is not registered in app.extensions'
        )
    return service


def get_user_session_tracking_service() -> UserSessionTrackingService:
    service = current_app.extensions['user_session_tracking_service']
    if service is None:
        raise RuntimeError('[ERROR] UserSessionTrackingService is not registered in app.extensions')
    return service


def get_app_runtime_profile() -> ConfigAppRuntimeProfile:
    service = current_app.extensions['app_runtime_profile']
    if service is None:
        raise RuntimeError('[ERROR] ConfigAppRuntimeProfile is not registered in app.extensions')
    return service
