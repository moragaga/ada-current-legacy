from __future__ import annotations

import time

from dash import Input, Output, State, no_update, ALL, ctx
from dash.exceptions import PreventUpdate

from src.shared.time.timestamps import parse_utc_datetime
from datetime import datetime
import pytz

from src.app.dash.runtime import get_dash_app
from src.app.dependencies import get_app_runtime_profile, get_dashboard_context_service
from src.shared.runtime.logging.debug import debug_log
from src.shared.ui.app_dashboard_shell.runtime.ids import DashboardRuntimeShellIds

from ..services.dashboard_runtime_refresh import (
    build_acquired_dashboard_refresh_lock,
    build_dashboard_refresh_signal,
    build_released_dashboard_refresh_lock,
    evaluate_dashboard_runtime_result,
    is_dashboard_refresh_lock_expired,
)
from ..services.dashboard_runtime_store_specs import build_dashboard_runtime_store_specs_for_profile
from ..services.normalize_stores_mapper import (
    build_normalized_runtime_stores,
    rebuild_runtime_stores_from_current_state,
)


_BACKDROP_CLASS_NAME = 'display-card-backdrop'

_BACKDROP_VISIBLE_CLASS_NAME = (
    'display-card-backdrop '
    'display-card-backdrop--visible'
)

TOTAL_BACKDROPS = 24

def register_dashboard_runtime_refresh_callback() -> None:
    app = get_dash_app()
    app_runtime_profile = get_app_runtime_profile()
    profile = app_runtime_profile.get_profile_value()

    store_specs = build_dashboard_runtime_store_specs_for_profile(profile=profile)

    debug_log(
        '[INFO] Register dashboard runtime refresh callback | profile={0} | stores={1}'.format(
            profile.value,
            [spec.store_id for spec in store_specs],
        )
    )

    runtime_outputs = [
        Output(component_id=spec.store_id, component_property='data') for spec in store_specs
    ]

    runtime_states = [
        State(component_id=spec.store_id, component_property='data') for spec in store_specs
    ]

    @app.callback(
        Output(
            component_id=DashboardRuntimeShellIds.STORE_REFRESH_SIGNAL,
            component_property='data',
            allow_duplicate=True,
        ),
        Input(
            component_id=DashboardRuntimeShellIds.INTERVAL_DASHBOARD,
            component_property='n_intervals',
        ),
        State(
            component_id=DashboardRuntimeShellIds.STORE_REFRESH_LOCK,
            component_property='data',
        ),
        prevent_initial_call='initial_duplicate',
    )
    def request_dashboard_runtime_refresh(n_intervals, lock_data):
        if n_intervals is None:
            raise PreventUpdate

        lock_data = lock_data or {}

        if lock_data.get('is_running', False) and not is_dashboard_refresh_lock_expired(
            lock_data=lock_data,
        ):
            raise PreventUpdate

        signal = build_dashboard_refresh_signal()

        debug_log(
            '[INFO] Dashboard runtime refresh request | token={0} | n_intervals={1}'.format(
                signal.get('token'),
                n_intervals,
            )
        )

        return signal

    @app.callback(
        Output(
            component_id=DashboardRuntimeShellIds.STORE_REFRESH_LOCK,
            component_property='data',
            allow_duplicate=True,
        ),
        Input(
            component_id=DashboardRuntimeShellIds.STORE_REFRESH_SIGNAL,
            component_property='data',
        ),
        State(
            component_id=DashboardRuntimeShellIds.STORE_REFRESH_LOCK,
            component_property='data',
        ),
        prevent_initial_call=True,
    )
    def acquire_dashboard_runtime_refresh_lock(signal_data, lock_data):
        if not signal_data:
            raise PreventUpdate

        lock_data = lock_data or {}

        if lock_data.get('is_running', False) and not is_dashboard_refresh_lock_expired(
            lock_data=lock_data,
        ):
            raise PreventUpdate

        acquired_lock = build_acquired_dashboard_refresh_lock(signal=signal_data)

        debug_log(
            '[INFO] Dashboard runtime refresh lock acquired | token={0}'.format(
                acquired_lock.get('active_token'),
            )
        )

        return acquired_lock

    @app.callback(
        *runtime_outputs,
        Output(
            component_id=DashboardRuntimeShellIds.STORE_INFORMATION_STATUS,
            component_property='data',
        ),
        Output(
            component_id=DashboardRuntimeShellIds.STORE_REFRESH_LOCK,
            component_property='data',
            allow_duplicate=True,
        ),
        Input(
            component_id=DashboardRuntimeShellIds.STORE_REFRESH_LOCK,
            component_property='data',
        ),
        State(
            component_id=DashboardRuntimeShellIds.STORE_REFRESH_SIGNAL,
            component_property='data',
        ),
        *runtime_states,
        State(
            component_id=DashboardRuntimeShellIds.STORE_INFORMATION_STATUS,
            component_property='data',
        ),
        prevent_initial_call=True,
    )
    def refresh_dashboard_runtime_data(lock_data, signal_data, *state_values):
        if not lock_data:
            raise PreventUpdate

        if not lock_data.get('is_running', False):
            raise PreventUpdate

        active_token = lock_data.get('active_token')
        signal_token = (signal_data or {}).get('token')

        if not active_token:
            raise PreventUpdate

        if active_token != signal_token:
            debug_log(
                '[WARN] Ignoring stale dashboard runtime refresh | active_token={0} | signal_token={1}'.format(
                    active_token,
                    signal_token,
                )
            )
            raise PreventUpdate

        current_store_values = list(state_values[:-1])
        information_status_store = state_values[-1] if state_values else {}
        information_status_store = information_status_store or {}

        start = time.perf_counter()

        try:
            service = get_dashboard_context_service()
            previous_last_update_pi_utc = information_status_store.get('last_update_pi_utc')
            previous_last_update_dispatch_utc = information_status_store.get('last_update_dispatch_utc')
            current_last_update = service.get_dashboard_latest_update()

            runtime_store, information_status_store, changed = evaluate_dashboard_runtime_result(
                current_last_update=current_last_update,
                previous_last_update_pi_utc=previous_last_update_pi_utc,
                previous_last_update_dispatch_utc=previous_last_update_dispatch_utc,
            )

            if changed or current_last_update is None:
                context = service.get_dashboard_context()
                runtime_payloads = build_normalized_runtime_stores(
                    context=context,
                    store_specs=store_specs,
                    runtime_store=runtime_store,
                )
            else:
                runtime_payloads = rebuild_runtime_stores_from_current_state(
                    current_store_values=current_store_values,
                    runtime_store=runtime_store,
                )

            elapsed = time.perf_counter() - start

            debug_log(
                '[INFO] Dashboard runtime refresh success | token={0} | elapsed={1:.2f} | changed={2} | expired={3} | last_update_pi_utc={4}'.format(
                    active_token,
                    elapsed,
                    runtime_store.get('changed'),
                    information_status_store.get('expired'),
                    information_status_store.get('last_update_pi_utc'),
                )
            )
            return (
                *runtime_payloads,
                information_status_store,
                build_released_dashboard_refresh_lock(),
            )

        except Exception as exception:
            debug_log(
                '[ERROR] Dashboard runtime refresh failed | token={0} | exception={1}'.format(
                    active_token,
                    exception,
                )
            )

            return (
                *([no_update] * len(store_specs)),
                no_update,
                build_released_dashboard_refresh_lock(),
            )

    @app.callback(
        Output(
            component_id={
                'type': 'display-card-status-backdrop',
                'index': ALL,
            },
            component_property='className',
        ),
        Input(
            component_id=DashboardRuntimeShellIds.STORE_INFORMATION_STATUS,
            component_property='data',
        ),
        State(
            component_id={
                'type': 'display-card-status-backdrop',
                'index': ALL,
            },
            component_property='id',
        ),
    )
    def update_display_card_backdrops(
        context,
        backdrop_ids,
    ) -> list[str]:
        if ctx.triggered_id is None or context is None:
            raise PreventUpdate

        if len(backdrop_ids) < TOTAL_BACKDROPS:
            raise PreventUpdate

        _start = time.perf_counter()

        last_update_pi = parse_utc_datetime(context.get('last_update_pi_utc'))

        if last_update_pi is None:
            has_critical_delay = True
        else:
            now = datetime.now(pytz.utc)
            has_critical_delay = (now - last_update_pi).total_seconds() > 60 * 15


        class_name = resolve_backdrop_class_name(
            is_visible=has_critical_delay,
        )

        debug_log(f'[INFO] render backdrop time took {time.perf_counter() - _start:.2f} seconds.')

        return [
            class_name
            for _ in backdrop_ids
        ]

def resolve_backdrop_class_name(
    *,
    is_visible: bool,
) -> str:
    if is_visible:
        return _BACKDROP_VISIBLE_CLASS_NAME

    return _BACKDROP_CLASS_NAME