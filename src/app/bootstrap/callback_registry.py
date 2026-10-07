from __future__ import annotations


def register_dash_callbacks() -> None:
    _register_navigation_callbacks()
    _register_dashboard_callbacks()
    _register_admin_callbacks()
    _register_alarm_monitor_callbacks()
    _register_alarm_panel_callbacks()
    _register_alarm_management_message_admin_callbacks()
    _register_alarm_management_image_admin_callbacks()
    _register_alarm_definition_images_modal_callbacks()
    _register_alarm_management_callbacks()
    _register_identity_users_admin_callbacks()
    _register_user_sessions_analytics_page_callbacks()


def _register_navigation_callbacks() -> None:
    from src.app.navigation import (
        register_app_navigation_callbacks,
    )

    register_app_navigation_callbacks()


def _register_dashboard_callbacks() -> None:
    from src.features.dashboards.home import register_dashboard_home_callbacks

    register_dashboard_home_callbacks()


def _register_alarm_monitor_callbacks() -> None:
    from src.features.alarm_monitor.callbacks import (
        register_distributed_alarm_monitor_refresh_callback,
        # register_generic_alarm_monitor_refresh_callback
    )

    register_distributed_alarm_monitor_refresh_callback()
    # register_generic_alarm_monitor_refresh_callback()


def _register_admin_callbacks() -> None:
    from src.features.configuration.admin_panels.alarm_configuration.callbacks import (
        register_alarm_configuration_admin_callback,
    )
    from src.features.configuration.admin_panels.kpi_configuration.callbacks import (
        register_kpi_configuration_admin_callback,
    )
    from src.features.configuration.admin_panels.navigation.groups.callbacks import (
        register_navigation_groups_admin_callback,
    )
    from src.features.configuration.admin_panels.navigation.links.callbacks import (
        register_navigation_links_admin_callback,
    )
    from src.features.configuration.admin_panels.publication_manager.callbacks import (
        register_publication_manager_callback,
    )

    register_navigation_groups_admin_callback()
    register_navigation_links_admin_callback()
    register_publication_manager_callback()
    register_kpi_configuration_admin_callback()
    register_alarm_configuration_admin_callback()


def _register_alarm_panel_callbacks():
    # from src.features.alarm_monitor.panel import (
    #     register_alarm_panel_callbacks,
    # )
    from src.features.alarm_monitor.feedback.active_alarms_modal.callbacks import (
        register_active_alarms_modal_callbacks,
    )
    from src.features.alarm_monitor.feedback.managed_alarms_modal.callbacks import (
        register_managed_alarms_modal_callbacks,
    )
    from src.features.alarm_monitor.panel_distributed import (
        register_distributed_alarm_panel_callback,
    )

    register_distributed_alarm_panel_callback()
    # register_alarm_panel_callbacks()
    register_active_alarms_modal_callbacks()
    register_managed_alarms_modal_callbacks()


def _register_alarm_management_message_admin_callbacks():
    from src.features.configuration.admin_panels.alarm_management.messages.callbacks import (
        register_alarm_management_message_admin_callback,
    )

    register_alarm_management_message_admin_callback()


def _register_alarm_management_image_admin_callbacks():
    from src.features.configuration.admin_panels.alarm_management.images.callbacks import (
        register_alarm_management_image_admin_callback,
    )

    register_alarm_management_image_admin_callback()


def _register_alarm_definition_images_modal_callbacks():
    from src.features.alarm_monitor.feedback.alarm_definition_images_modal.callbacks import (
        register_alarm_definition_images_modal_callbacks,
    )

    register_alarm_definition_images_modal_callbacks()


def _register_alarm_management_callbacks() -> None:
    # from src.features.alarm_management.operator import (
    #     register_alarm_management_operator_callbacks,
    # )

    from src.features.alarm_management.distributed_operator import (
        register_distributed_alarm_bulk_management_callback,
        register_distributed_alarm_management_operator_callback,
    )

    # Genérico: no activo en esta app por ahora.
    # register_alarm_management_operator_callbacks()

    register_distributed_alarm_management_operator_callback()
    register_distributed_alarm_bulk_management_callback()


def _register_identity_users_admin_callbacks():
    from src.features.configuration.admin_panels.identity.users.callbacks import (
        register_identity_users_admin_callback,
    )

    register_identity_users_admin_callback()


def _register_user_sessions_analytics_page_callbacks():
    from src.features.user_sessions.callbacks import (
        register_user_session_analytics_callbacks,
    )

    register_user_session_analytics_callbacks()
