# # DESCOMENTAR CUANDO SE UTILICE EL PROCESO GENERICO
# from __future__ import annotations
#
# import time
#
# from dash import (
#     Input,
#     Output,
#     State,
#     no_update
# )
# from dash.exceptions import PreventUpdate
#
# from src.app.dash import get_dash_app
# from src.app.dependencies import get_generic_alarm_context_service
# from src.shared.runtime.logging.debug import debug_log
# from src.shared.ui.app_alarm_shell.ids import AlarmShellIds
# from src.features.basic_analytics_runtime.managed_alarms.services import (
#     get_managed_alarm_analytics_runtime_service,
# )
# from ..services.runtime_refresh import (
#     build_acquire_lock,
#     build_release_lock,
#     is_lock_expired,
# )
#
#
# def register_generic_alarm_monitor_refresh_callback() -> None:
#     app = get_dash_app()
#
#     @app.callback(
#         Output(
#             component_id=AlarmShellIds.STORE_ALARM_REFRESH_LOCK,
#             component_property='data',
#             allow_duplicate=True,
#         ),
#         Input(
#             component_id=AlarmShellIds.INTERVAL_ALARMS,
#             component_property='n_intervals',
#         ),
#         State(
#             component_id=AlarmShellIds.STORE_ALARM_REFRESH_LOCK,
#             component_property='data',
#         ),
#         prevent_initial_call='initial_duplicate',
#     )
#     def acquire_generic_alarm_monitor_refresh_lock(
#         n_intervals,
#         lock_data,
#     ):
#         if n_intervals is None:
#             raise PreventUpdate
#
#         lock_data = lock_data or {}
#
#         if lock_data.get('is_running', False) and not is_lock_expired(
#             lock_data=lock_data,
#         ):
#             raise PreventUpdate
#
#         debug_log('[INFO] Generic alarm refresh lock acquired')
#         return build_acquire_lock()
#
#     @app.callback(
#         Output(
#             component_id=AlarmShellIds.STORE_ALARM_RUNTIME_STORE,
#             component_property='data',
#         ),
#         Output(
#             component_id=AlarmShellIds.STORE_ALARM_RESUME_STORE,
#             component_property='data',
#         ),
#         Output(
#             component_id=AlarmShellIds.STORE_ALARM_REFRESH_LOCK,
#             component_property='data',
#             allow_duplicate=True,
#         ),
#         Input(
#             component_id=AlarmShellIds.STORE_ALARM_REFRESH_LOCK,
#             component_property='data',
#         ),
#         prevent_initial_call=True,
#     )
#     def refresh_generic_alarm_monitor_data(lock_data):
#         lock_data = lock_data or {}
#
#         if not lock_data:
#             raise PreventUpdate
#
#         if not lock_data.get('is_running', False):
#             raise PreventUpdate
#
#         start = time.perf_counter()
#
#         try:
#             service = get_generic_alarm_context_service()
#             context = service.get_alarm_context() or {}
#
#             current_turn_management_count = (
#                 get_managed_alarm_analytics_runtime_service()
#                 .get_current_turn_management_count()
#             )
#
#             elapsed = time.perf_counter() - start
#
#             debug_log(
#                 '[INFO] Distributed alarm refresh success | '
#                 'elapsed={0:.4f} | last_updated={1} | '
#                 'active_alarms={2} | active_managed_alarms={3} | total_alarms={4} | '
#                 'total_managed_alarms={5}'.format(
#                     elapsed,
#                     context.get('last_updated', ''),
#                     context.get('total_active_alarms'),
#                     context.get('total_active_managed_alarms'),
#                     context.get('total_alarms'),
#                     current_turn_management_count
#                 )
#             )
#
#             return (
#                 context,
#                 {
#                     'mode': context.get('mode', 'generic'),
#                     'total_active_alarms': context.get('total_active_alarms', 0),
#                     'total_active_managed_alarms': context.get(
#                         'total_active_managed_alarms',
#                         0,
#                     ),
#                     'total_alarms': context.get('total_alarms', 0),
#                     'total_managed_alarms': current_turn_management_count,
#                 },
#                 build_release_lock(),
#             )
#
#         except Exception as error:
#             debug_log(
#                 '[ERROR] Generic alarm refresh failed | exception={0}'.format(
#                     error,
#                 )
#             )
#
#             return no_update, no_update, build_release_lock()
