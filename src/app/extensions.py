from __future__ import annotations

from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager

from ..features.admin_framework.services import AdminDataService
from ..features.alarm_management.core.services import (
    AlarmManagementActionBuilder,
    AlarmManagementCommandService,
    AlarmManagementContextService,
    AlarmManagementUseCaseService,
)
from ..features.alarm_management.infrastructure.repositories import (
    AlarmManagementActionRepository,
    CosmosAlarmManagementRuntimeInputProvider,
)
from ..features.alarm_management.infrastructure.services import (
    TwoTurnShiftEndProvider,
)
from ..features.alarm_management.infrastructure.settings import (
    AlarmManagementRuntimeSettings,
)

# Activar cuando exista una app genérica usando alarm_monitor/panel.
# from src.features.alarm_runtime.front_context.generic import GenericAlarmContextService
from ..features.alarm_runtime.front_context.distributed import DistributedAlarmContextService
from ..features.alarm_runtime.repositories import AlarmRepository
from ..features.alarm_runtime.services import AlarmQueryService
from ..features.alarm_runtime.settings import AlarmRuntimeSettings
from ..features.configuration.admin_panels.alarm_management.messages.services import (
    AlarmMessageAdminService,
)
from ..features.configuration.admin_panels.publication_manager.services import (
    PublicationManagerActionService,
)
from ..features.configuration.repositories import (
    ConfigManifestRepository,
    ConfigPublicationStateRepository,
    ConfigurationSharepointRepository,
)
from ..features.configuration.services import (
    ConfigHashService,
    ConfigManifestService,
    ConfigManifestSyncService,
    ConfigPublicationService,
    ConfigService,
    ConfigStatusService,
    build_config_artifact_registry,
)
from ..features.configuration.services.config_app_runtime_profile import ConfigAppRuntimeProfile
from ..features.configuration.services.config_first_projection_sync_service import (
    ConfigFirstProjectionSyncService,
)
from ..features.dashboard_runtime.repositories import (
    DashboardSnapshotRepository,
    KpiConfigurationRepository,
)
from ..features.dashboard_runtime.services import (
    DashboardContextService,
    DashboardQueryService,
    KpiConfigurationContextService,
    KpiConfigurationQueryService,
)
from ..features.dashboard_runtime.settings import (
    DashboardRuntimeSettings,
    KpiConfigurationRuntimeSettings,
)
from ..features.identity.repositories import (
    SharePointIdentityRepository,
)
from ..features.identity.services import IdentitySyncService
from ..features.identity.services.identity_first_projection_sync_service import (
    IdentityFirstProjectionSyncService,
)
from ..features.identity.settings import get_identity_settings
from ..features.navigation.repositories import (
    NavigationProjectionRepository,
)
from ..features.navigation.services import (
    NavigationCacheService,
    NavigationFirstProjectionSyncService,
    NavigationReadService,
)
from ..features.user_sessions.repositories import UserSessionRepository
from ..features.user_sessions.services import (
    UserSessionTrackingService,
    UserSessionTrackingSettings,
)
from ..shared.infrastructure.cosmos import (
    CosmosService,
    CosmosSettings,
    create_cosmos_client,
    ensure_required_containers,
    ensure_required_database,
)
from ..shared.infrastructure.sharepoint import SharepointService, SharepointSettings
from .env_configuration import EnvConfiguration


def init_extensions(app: Flask, settings: EnvConfiguration) -> None:
    app.extensions = getattr(app, 'extensions', {})

    _init_configuration_app_runtime_profile(app=app, settings=settings)
    _init_cosmos(app=app, settings=settings)
    _init_sharepoint(app=app, settings=settings)
    _init_base_extensions(app=app)
    _init_login_manager(app=app)
    _init_identity_services(app=app)
    _init_configuration_services(app=app)
    _init_alarm_management_admin_services(app=app)
    _init_publication_services(app=app)
    _init_navigation_cache_services(app=app, settings=settings)
    _init_kpi_configuration_runtime(app=app)
    _init_dashboard_runtime(app=app)
    _init_distributed_alarm_context_service(app=app)
    # Activar cuando exista una app genérica usando alarm_monitor/panel.
    # _init_generic_alarm_context_service(app)
    _init_alarm_management_operator_services(app=app)
    _init_user_session_tracking_service(app=app, settings=settings)
    # Evaluate to args
    if settings.is_first_load:
        _init_navigation_first_projection(app=app, settings=settings)
        _init_identity_first_projection(app=app)
        _init_configuration_first_projection(app=app, settings=settings)
    _init_cors(app=app)


def _init_cosmos(app: Flask, settings: EnvConfiguration) -> None:
    cosmos_settings = CosmosSettings.from_env(settings=settings)
    client = create_cosmos_client(settings=cosmos_settings)

    if not settings.is_remote_service:
        print('[INFO] Init with local runtime')
        ensure_required_database(client=client, settings=cosmos_settings)
        print(
            f'[INFO] local runtime - {cosmos_settings.database_name} database create successfully'
        )

    service = CosmosService(client=client, database_name=cosmos_settings.database_name)
    ensure_required_containers(cosmos_service=service, is_remote_service=settings.is_remote_service)

    app.extensions['cosmos_service'] = service


def _init_base_extensions(app: Flask) -> None:
    extensions = ()
    for extension in extensions:
        app.extensions[extension] = {}


def _init_login_manager(app: Flask) -> None:
    login_manager = LoginManager()
    login_manager.init_app(app)
    app.extensions['login_manager'] = login_manager


def _init_identity_services(app: Flask) -> None:
    sharepoint_service: SharepointService | None = app.extensions.get('sharepoint_service')

    with app.app_context():
        identity_settings = get_identity_settings()

    configuration_repository = ConfigurationSharepointRepository(
        sharepoint_service=sharepoint_service,
    )

    sharepoint_repository = SharePointIdentityRepository(
        repository=configuration_repository,
        settings=identity_settings,
    )

    app.extensions['identity_sync_service'] = IdentitySyncService(
        sharepoint_repository=sharepoint_repository,
        settings=identity_settings,
    )
    app.extensions['sharepoint_identity_repository'] = sharepoint_repository


def _init_configuration_services(app: Flask) -> None:
    sharepoint_service = app.extensions.get('sharepoint_service')
    app_runtime_profile = app.extensions.get('app_runtime_profile')

    configuration_sharepoint_repository = ConfigurationSharepointRepository(
        sharepoint_service=sharepoint_service,
    )
    config_service = ConfigService()

    config_manifest_repository = ConfigManifestRepository(
        repository=configuration_sharepoint_repository,
    )
    config_hash_service = ConfigHashService()
    config_artifact_registry = build_config_artifact_registry(
        app_runtime_profile=app_runtime_profile
    )

    config_manifest_service = ConfigManifestService(
        repository=config_manifest_repository,
        hash_service=config_hash_service,
    )

    config_manifest_sync_service = ConfigManifestSyncService(
        registry=config_artifact_registry,
        manifest_repository=config_manifest_repository,
        configuration_repository=configuration_sharepoint_repository,
        hash_service=config_hash_service,
    )

    app.extensions['configuration_sharepoint_repository'] = configuration_sharepoint_repository
    app.extensions['config_service'] = config_service
    app.extensions['config_manifest_repository'] = config_manifest_repository
    app.extensions['config_hash_service'] = config_hash_service
    app.extensions['config_artifact_registry'] = config_artifact_registry
    app.extensions['config_manifest_service'] = config_manifest_service
    app.extensions['config_manifest_sync_service'] = config_manifest_sync_service


def _init_publication_services(app: Flask) -> None:
    cosmos_service: CosmosService = app.extensions.get('cosmos_service')
    config_manifest_repository: ConfigManifestRepository = app.extensions.get(
        'config_manifest_repository'
    )
    configuration_repository: ConfigurationSharepointRepository = app.extensions.get(
        'configuration_sharepoint_repository'
    )
    config_manifest_sync_service = app.extensions.get('config_manifest_sync_service')

    config_publication_state_repository = ConfigPublicationStateRepository(
        cosmos_service=cosmos_service,
    )

    config_status_service = ConfigStatusService(
        manifest_repository=config_manifest_repository,
        publication_state_repository=config_publication_state_repository,
    )

    config_publication_service = ConfigPublicationService(
        manifest_repository=config_manifest_repository,
        publication_state_repository=config_publication_state_repository,
        configuration_repository=configuration_repository,
        cosmos_service=cosmos_service,
    )

    publication_manager_action_service = PublicationManagerActionService(
        status_service=config_status_service,
        publication_service=config_publication_service,
        manifest_sync_service=config_manifest_sync_service,
    )

    app.extensions['config_publication_state_repository'] = config_publication_state_repository
    app.extensions['config_status_service'] = config_status_service
    app.extensions['config_publication_service'] = config_publication_service
    app.extensions['publication_manager_action_service'] = publication_manager_action_service


def _init_navigation_cache_services(app: Flask, settings: EnvConfiguration) -> None:
    cosmos_service: CosmosService = app.extensions['cosmos_service']

    projection_repository = NavigationProjectionRepository(
        cosmos_service=cosmos_service,
    )

    read_service = NavigationReadService(
        projection_repository=projection_repository, app_name=settings.app_name
    )

    app.extensions['navigation_cache_service'] = NavigationCacheService(
        read_service=read_service,
        ttl_seconds=300,
    )


def _init_sharepoint(app: Flask, settings: EnvConfiguration) -> None:
    sharepoint_settings = SharepointSettings.from_env(settings=settings)
    service = SharepointService(settings=sharepoint_settings)
    app.extensions['sharepoint_service'] = service


def _init_kpi_configuration_runtime(app: Flask) -> None:
    cosmos_service: CosmosService = app.extensions.get('cosmos_service')
    runtime_settings = KpiConfigurationRuntimeSettings.from_env()

    repository = KpiConfigurationRepository(
        cosmos_service=cosmos_service,
        settings=runtime_settings,
    )

    query_service = KpiConfigurationQueryService(
        kpi_configuration_repository=repository,
    )

    context_service = KpiConfigurationContextService(
        kpi_configuration_query_service=query_service,
    )

    app.extensions['kpi_configuration_context_service'] = context_service


def _init_distributed_alarm_context_service(app: Flask) -> None:
    cosmos_service: CosmosService = app.extensions.get('cosmos_service')
    runtime_settings = AlarmRuntimeSettings.from_env()

    repository = AlarmRepository(
        cosmos_service=cosmos_service,
        settings=runtime_settings,
    )

    alarm_query_service = AlarmQueryService(
        alarm_repository=repository,
    )

    context_service = DistributedAlarmContextService(
        query_service=alarm_query_service,
    )

    app.extensions['distributed_alarm_context_service'] = context_service


# # Activar cuando exista una app genérica usando alarm_monitor/panel.
# def _init_generic_alarm_context_service(app) -> None:
#     cosmos_service: CosmosService = app.extensions.get('cosmos_service')
#     runtime_settings = AlarmRuntimeSettings.from_env()
#
#     alarm_repository = AlarmRepository(
#         cosmos_service=cosmos_service,
#         settings=runtime_settings,
#     )
#
#     alarm_query_service = AlarmQueryService(
#         alarm_repository=alarm_repository,
#     )
#
#     context_service = GenericAlarmContextService(
#         query_service=alarm_query_service,
#     )
#
#     app.extensions['generic_alarm_context_service'] = context_service


def _init_dashboard_runtime(app: Flask) -> None:
    cosmos_service: CosmosService = app.extensions.get('cosmos_service')
    runtime_settings = DashboardRuntimeSettings.from_env()
    # kpi_configuration_context_service: KpiConfigurationContextService = app.extensions.get(
    #     'kpi_configuration_context_service'
    # )
    app_runtime_profile: ConfigAppRuntimeProfile = app.extensions.get('app_runtime_profile')

    snapshot_repository = DashboardSnapshotRepository(
        cosmos_service=cosmos_service,
        settings=runtime_settings,
    )

    query_service = DashboardQueryService(snapshot_repository=snapshot_repository)

    context_service = DashboardContextService(
        dashboard_query_service=query_service, app_runtime_profile=app_runtime_profile
    )

    app.extensions['dashboard_context_service'] = context_service


def _init_alarm_management_admin_services(app: Flask) -> None:
    configuration_repository: ConfigurationSharepointRepository = app.extensions.get(
        'configuration_sharepoint_repository'
    )
    config_service: ConfigService = app.extensions.get('config_service')
    config_manifest_service: ConfigManifestService = app.extensions.get('config_manifest_service')

    alarm_message_admin_service = AlarmMessageAdminService(
        admin_data_service=AdminDataService(
            repository=configuration_repository,
            config_service=config_service,
        ),
        configuration_repository=configuration_repository,
        manifest_service=config_manifest_service,
    )

    app.extensions['alarm_message_admin_service'] = alarm_message_admin_service


def _init_alarm_management_operator_services(app: Flask) -> None:
    cosmos_service: CosmosService = app.extensions.get('cosmos_service')

    alarm_management_runtime_settings = AlarmManagementRuntimeSettings()

    alarm_management_shift_end_provider = TwoTurnShiftEndProvider()

    alarm_management_runtime_input_provider = CosmosAlarmManagementRuntimeInputProvider(
        cosmos_service=cosmos_service,
        settings=alarm_management_runtime_settings,
        shift_end_provider=alarm_management_shift_end_provider,
    )

    alarm_management_action_repository = AlarmManagementActionRepository(
        cosmos_service=cosmos_service,
        container_name=alarm_management_runtime_settings.action_container_name,
    )

    alarm_management_action_builder = AlarmManagementActionBuilder()

    alarm_management_context_service = AlarmManagementContextService()

    alarm_management_command_service = AlarmManagementCommandService(
        action_builder=alarm_management_action_builder,
        action_repository=alarm_management_action_repository,
    )

    alarm_management_use_case_service = AlarmManagementUseCaseService(
        runtime_input_provider=alarm_management_runtime_input_provider,
        context_service=alarm_management_context_service,
        command_service=alarm_management_command_service,
    )

    app.extensions['alarm_management_runtime_settings'] = alarm_management_runtime_settings
    app.extensions['alarm_management_shift_end_provider'] = alarm_management_shift_end_provider
    app.extensions['alarm_management_runtime_input_provider'] = (
        alarm_management_runtime_input_provider
    )
    app.extensions['alarm_management_action_repository'] = alarm_management_action_repository
    app.extensions['alarm_management_action_builder'] = alarm_management_action_builder
    app.extensions['alarm_management_context_service'] = alarm_management_context_service
    app.extensions['alarm_management_command_service'] = alarm_management_command_service
    app.extensions['alarm_management_use_case_service'] = alarm_management_use_case_service


def _init_user_session_tracking_service(app: Flask, settings: EnvConfiguration) -> None:
    cosmos_service: CosmosService = app.extensions.get('cosmos_service')

    user_session_tracking_settings = UserSessionTrackingSettings.from_env(settings=settings)

    repository = UserSessionRepository(
        cosmos_service=cosmos_service,
        settings=user_session_tracking_settings,
    )

    app.extensions['user_session_tracking_service'] = UserSessionTrackingService(
        repository=repository,
        settings=user_session_tracking_settings,
    )


def _init_configuration_first_projection(app: Flask, settings: EnvConfiguration) -> None:
    print('[INFO] Init configuration first remote projection')
    cosmos_service: CosmosService = app.extensions.get('cosmos_service')
    publication_manager_action_service: PublicationManagerActionService = app.extensions[
        'publication_manager_action_service'
    ]

    ConfigFirstProjectionSyncService(
        cosmos_service=cosmos_service,
        publication_manager_action_service=publication_manager_action_service,
        settings=settings,
    ).sync_first_remote_projection()


def _init_navigation_first_projection(app: Flask, settings: EnvConfiguration) -> None:
    print('[INFO] Init navigation first local projection')
    configuration_repository: ConfigurationSharepointRepository = app.extensions.get(
        'configuration_sharepoint_repository'
    )
    config_service: ConfigService = app.extensions.get('config_service')
    config_manifest_service: ConfigManifestService = app.extensions.get('config_manifest_service')

    NavigationFirstProjectionSyncService(
        sharepoint_repository=configuration_repository,
        config_service=config_service,
        config_manifest_service=config_manifest_service,
        app_name=settings.app_name,
    ).sync_first_local_projection()


def _init_identity_first_projection(app: Flask) -> None:
    print('[INFO] Init identities first local projection')
    sharepoint_identity_repository: SharePointIdentityRepository = app.extensions[
        'sharepoint_identity_repository'
    ]

    IdentityFirstProjectionSyncService(
        sharepoint_identity_repository=sharepoint_identity_repository,
    ).sync_first_local_projection()


def _init_configuration_app_runtime_profile(app: Flask, settings: EnvConfiguration) -> None:
    app_runtime_profile = ConfigAppRuntimeProfile(
        settings=settings,
    )
    app.extensions['app_runtime_profile'] = app_runtime_profile


def _init_cors(app: Flask) -> None:
    CORS(
        app,
        resources={
            r'/logout': {'origins': '*'},
            r'/assets/manifest.json': {'origins': '*'},
            r'/api/*': {'origins': '*'},
        },
        supports_credentials=True,
    )
