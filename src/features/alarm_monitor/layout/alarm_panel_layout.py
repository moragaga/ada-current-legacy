from __future__ import annotations

from src.features.alarm_management.distributed_operator.builders import (
    build_distributed_alarm_management_modal_host,
)
from src.shared.ui.app_alarm_shell.app_alarm_shell import build_app_alarm_shell

from ..feedback.active_alarms_modal.builders.active_alarm_modal_host import (
    build_active_alarms_modal_host,
)
from ..feedback.alarm_definition_images_modal.builders import (
    build_alarm_definition_images_modal_host,
)
from ..feedback.managed_alarms_modal.builders import (
    build_managed_alarms_modal_host,
)

# Flujo genérico. Activar cuando la app use alarm_monitor/panel + alarm_management/operator.
# from ..panel.builders import (
#     build_alarm_panel,
#     build_alarm_panel_ready_flag,
# )
# from src.features.alarm_management.operator.builders import (
#     build_alarm_management_modal_host,
# )
# Flujo distribuido. App actual.
from ..panel_distributed.builders import (
    build_distributed_alarm_panel,
    build_distributed_alarm_panel_ready_flag,
)


def build_alarm_panel_layout():
    return build_app_alarm_shell(
        children=[
            # Flujo genérico.
            # build_alarm_panel(),
            # build_alarm_panel_ready_flag(),
            # build_alarm_management_modal_host(),
            # Flujo distribuido.
            build_distributed_alarm_panel(),
            build_distributed_alarm_panel_ready_flag(),
            build_distributed_alarm_management_modal_host(),
            build_active_alarms_modal_host(),
            build_managed_alarms_modal_host(),
            build_alarm_definition_images_modal_host(),
        ],
    )
