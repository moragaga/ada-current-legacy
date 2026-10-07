from __future__ import annotations

from typing import Any

from dash import Input, Output, State, ctx
from dash.exceptions import PreventUpdate

from src.app.dash.runtime import get_dash_app
from src.shared.ui.app_alarm_shell.ids import AlarmShellIds

from .components.active_alarm_list import (
    build_alarm_list_children,
)
from .ids import ActiveAlarmsModalIds
from .services.active_alarm_modal_snapshot_mapper import (
    build_active_alarm_modal_snapshot,
    build_paginated_view,
    get_next_page,
    get_total_pages_for_source,
)


def register_active_alarms_modal_callbacks() -> None:
    app = get_dash_app()

    @app.callback(
        Output(
            component_id=ActiveAlarmsModalIds.MODAL,
            component_property='is_open',
            allow_duplicate=True,
        ),
        Output(
            component_id=ActiveAlarmsModalIds.FROZEN_SNAPSHOT_STORE,
            component_property='data',
            allow_duplicate=True,
        ),
        Output(
            component_id=ActiveAlarmsModalIds.SEARCH_INPUT,
            component_property='value',
            allow_duplicate=True,
        ),
        Output(
            component_id=ActiveAlarmsModalIds.SORT_SELECT_TIME,
            component_property='value',
            allow_duplicate=True,
        ),
        Output(
            component_id=ActiveAlarmsModalIds.FILTER_SELECT_CRITICITY,
            component_property='value',
            allow_duplicate=True,
        ),
        Output(
            component_id=ActiveAlarmsModalIds.LAST_UPDATED_TEXT,
            component_property='children',
            allow_duplicate=True,
        ),
        Input(component_id=ActiveAlarmsModalIds.OPEN_BUTTON, component_property='n_clicks'),
        State(component_id=ActiveAlarmsModalIds.MODAL, component_property='is_open'),
        State(component_id=AlarmShellIds.STORE_ALARM_RUNTIME_STORE, component_property='data'),
        prevent_initial_call=True,
    )
    def open_modal(
        n_clicks: int | None,
        is_open: bool,
        runtime_store: dict[str, Any] | None,
    ):
        if (
            ctx.triggered_id is None
            or n_clicks is None
            or not n_clicks
            or is_open
            or ctx.triggered_id != ActiveAlarmsModalIds.OPEN_BUTTON
        ):
            raise PreventUpdate

        return _build_modal_content(runtime_store=runtime_store)

    @app.callback(
        Output(
            component_id=ActiveAlarmsModalIds.MODAL,
            component_property='is_open',
            allow_duplicate=True,
        ),
        Output(
            component_id=ActiveAlarmsModalIds.FROZEN_SNAPSHOT_STORE,
            component_property='data',
            allow_duplicate=True,
        ),
        Output(
            component_id=ActiveAlarmsModalIds.SEARCH_INPUT,
            component_property='value',
            allow_duplicate=True,
        ),
        Output(
            component_id=ActiveAlarmsModalIds.SORT_SELECT_TIME,
            component_property='value',
            allow_duplicate=True,
        ),
        Output(
            component_id=ActiveAlarmsModalIds.FILTER_SELECT_CRITICITY,
            component_property='value',
            allow_duplicate=True,
        ),
        Output(
            component_id=ActiveAlarmsModalIds.LAST_UPDATED_TEXT,
            component_property='children',
            allow_duplicate=True,
        ),
        Input(component_id=ActiveAlarmsModalIds.REFRESH_BUTTON, component_property='n_clicks'),
        State(component_id=ActiveAlarmsModalIds.MODAL, component_property='is_open'),
        State(component_id=AlarmShellIds.STORE_ALARM_RUNTIME_STORE, component_property='data'),
        prevent_initial_call=True,
    )
    def refresh_modal(
        n_clicks: int | None,
        is_open: bool,
        runtime_store: dict[str, Any] | None,
    ):
        if (
            ctx.triggered_id is None
            or n_clicks is None
            or not is_open
            or not n_clicks
            or ctx.triggered_id != ActiveAlarmsModalIds.REFRESH_BUTTON
        ):
            raise PreventUpdate

        return _build_modal_content(runtime_store=runtime_store)

    @app.callback(
        Output(
            component_id=ActiveAlarmsModalIds.MODAL,
            component_property='is_open',
            allow_duplicate=True,
        ),
        Input(component_id=ActiveAlarmsModalIds.CLOSE_BUTTON, component_property='n_clicks'),
        prevent_initial_call=True,
    )
    def close_modal(n_clicks: int | None):
        if n_clicks is not None or ctx.triggered_id == ActiveAlarmsModalIds.CLOSE_BUTTON:
            return False

        raise PreventUpdate

    @app.callback(
        Output(component_id=ActiveAlarmsModalIds.OPERATOR_PAGE_STORE, component_property='data'),
        Input(
            component_id=ActiveAlarmsModalIds.OPERATOR_PREVIOUS_BUTTON,
            component_property='n_clicks',
        ),
        Input(
            component_id=ActiveAlarmsModalIds.OPERATOR_NEXT_BUTTON, component_property='n_clicks'
        ),
        Input(component_id=ActiveAlarmsModalIds.SEARCH_INPUT, component_property='value'),
        Input(component_id=ActiveAlarmsModalIds.SORT_SELECT_TIME, component_property='value'),
        Input(
            component_id=ActiveAlarmsModalIds.FILTER_SELECT_CRITICITY, component_property='value'
        ),
        Input(component_id=ActiveAlarmsModalIds.FROZEN_SNAPSHOT_STORE, component_property='data'),
        State(component_id=ActiveAlarmsModalIds.OPERATOR_PAGE_STORE, component_property='data'),
    )
    def update_operator_page(
        previous_clicks: int | None,
        next_clicks: int | None,
        search_text: str | None,
        sort_order_time: str | None,
        filter_criticity: str | None,
        snapshot: dict[str, Any] | None,
        current_page: int | None,
    ):
        triggered_id = ctx.triggered_id

        if triggered_id in {
            ActiveAlarmsModalIds.SEARCH_INPUT,
            ActiveAlarmsModalIds.SORT_SELECT_TIME,
            ActiveAlarmsModalIds.FILTER_SELECT_CRITICITY,
            ActiveAlarmsModalIds.FROZEN_SNAPSHOT_STORE,
        }:
            return 1

        total_pages = get_total_pages_for_source(
            snapshot=snapshot,
            source_key='operator_items',
            search_text=search_text,
            sort_order_time=sort_order_time,
            filter_criticity=filter_criticity,
            page_size=ActiveAlarmsModalIds.PAGE_SIZE,
        )

        if triggered_id == ActiveAlarmsModalIds.OPERATOR_PREVIOUS_BUTTON:
            return get_next_page(
                current_page=current_page,
                direction='previous',
                total_pages=total_pages,
            )

        if triggered_id == ActiveAlarmsModalIds.OPERATOR_NEXT_BUTTON:
            return get_next_page(
                current_page=current_page,
                direction='next',
                total_pages=total_pages,
            )

        return current_page or 1

    @app.callback(
        Output(component_id=ActiveAlarmsModalIds.OPERATOR_LIST, component_property='children'),
        Output(component_id=ActiveAlarmsModalIds.OPERATOR_COUNT, component_property='children'),
        Output(component_id=ActiveAlarmsModalIds.OPERATOR_PAGE_TEXT, component_property='children'),
        Output(
            component_id=ActiveAlarmsModalIds.OPERATOR_PREVIOUS_BUTTON,
            component_property='disabled',
        ),
        Output(
            component_id=ActiveAlarmsModalIds.OPERATOR_NEXT_BUTTON, component_property='disabled'
        ),
        Input(component_id=ActiveAlarmsModalIds.FROZEN_SNAPSHOT_STORE, component_property='data'),
        Input(component_id=ActiveAlarmsModalIds.SEARCH_INPUT, component_property='value'),
        Input(component_id=ActiveAlarmsModalIds.SORT_SELECT_TIME, component_property='value'),
        Input(
            component_id=ActiveAlarmsModalIds.FILTER_SELECT_CRITICITY, component_property='value'
        ),
        Input(component_id=ActiveAlarmsModalIds.OPERATOR_PAGE_STORE, component_property='data'),
    )
    def render_operator_pool(
        snapshot: dict[str, Any] | None,
        search_text: str | None,
        sort_order_time: str | None,
        filter_criticity: str | None,
        page: int | None,
    ):
        view = build_paginated_view(
            snapshot=snapshot,
            source_key='operator_items',
            search_text=search_text,
            sort_order_time=sort_order_time,
            filter_criticity=filter_criticity,
            page=page,
            page_size=ActiveAlarmsModalIds.PAGE_SIZE,
        )

        children = build_alarm_list_children(
            items=view['items'],
            panel_kind='operator',
            page_size=ActiveAlarmsModalIds.PAGE_SIZE,
            has_snapshot=bool(view['has_snapshot']),
            empty_by_filter=bool(view['empty_by_filter']),
        )

        count_label = f'{view["total_items"]} {"Activa" if view["total_items"] == 1 else "Activas"}'
        page_text = f'Página {view["page"]} de {view["total_pages"]}'

        return (
            children,
            count_label,
            page_text,
            not view['has_previous'],
            not view['has_next'],
        )

    @app.callback(
        Output(component_id=ActiveAlarmsModalIds.TRACKING_PAGE_STORE, component_property='data'),
        Input(
            component_id=ActiveAlarmsModalIds.TRACKING_PREVIOUS_BUTTON,
            component_property='n_clicks',
        ),
        Input(
            component_id=ActiveAlarmsModalIds.TRACKING_NEXT_BUTTON, component_property='n_clicks'
        ),
        Input(component_id=ActiveAlarmsModalIds.SEARCH_INPUT, component_property='value'),
        Input(component_id=ActiveAlarmsModalIds.SORT_SELECT_TIME, component_property='value'),
        Input(
            component_id=ActiveAlarmsModalIds.FILTER_SELECT_CRITICITY, component_property='value'
        ),
        Input(component_id=ActiveAlarmsModalIds.FROZEN_SNAPSHOT_STORE, component_property='data'),
        State(component_id=ActiveAlarmsModalIds.TRACKING_PAGE_STORE, component_property='data'),
    )
    def update_tracking_page(
        previous_clicks: int | None,
        next_clicks: int | None,
        search_text: str | None,
        sort_order_time: str | None,
        filter_criticity: str | None,
        snapshot: dict[str, Any] | None,
        current_page: int | None,
    ):
        triggered_id = ctx.triggered_id

        if triggered_id in {
            ActiveAlarmsModalIds.SEARCH_INPUT,
            ActiveAlarmsModalIds.SORT_SELECT_TIME,
            ActiveAlarmsModalIds.FILTER_SELECT_CRITICITY,
            ActiveAlarmsModalIds.FROZEN_SNAPSHOT_STORE,
        }:
            return 1

        total_pages = get_total_pages_for_source(
            snapshot=snapshot,
            source_key='tracking_items',
            search_text=search_text,
            sort_order_time=sort_order_time,
            filter_criticity=filter_criticity,
            page_size=ActiveAlarmsModalIds.PAGE_SIZE,
        )

        if triggered_id == ActiveAlarmsModalIds.TRACKING_PREVIOUS_BUTTON:
            return get_next_page(
                current_page=current_page,
                direction='previous',
                total_pages=total_pages,
            )

        if triggered_id == ActiveAlarmsModalIds.TRACKING_NEXT_BUTTON:
            return get_next_page(
                current_page=current_page,
                direction='next',
                total_pages=total_pages,
            )

        return current_page or 1

    @app.callback(
        Output(component_id=ActiveAlarmsModalIds.TRACKING_LIST, component_property='children'),
        Output(component_id=ActiveAlarmsModalIds.TRACKING_COUNT, component_property='children'),
        Output(component_id=ActiveAlarmsModalIds.TRACKING_PAGE_TEXT, component_property='children'),
        Output(
            component_id=ActiveAlarmsModalIds.TRACKING_PREVIOUS_BUTTON,
            component_property='disabled',
        ),
        Output(
            component_id=ActiveAlarmsModalIds.TRACKING_NEXT_BUTTON, component_property='disabled'
        ),
        Input(component_id=ActiveAlarmsModalIds.FROZEN_SNAPSHOT_STORE, component_property='data'),
        Input(component_id=ActiveAlarmsModalIds.SEARCH_INPUT, component_property='value'),
        Input(component_id=ActiveAlarmsModalIds.SORT_SELECT_TIME, component_property='value'),
        Input(
            component_id=ActiveAlarmsModalIds.FILTER_SELECT_CRITICITY, component_property='value'
        ),
        Input(component_id=ActiveAlarmsModalIds.TRACKING_PAGE_STORE, component_property='data'),
    )
    def render_tracking_view(
        snapshot: dict[str, Any] | None,
        search_text: str | None,
        sort_order_time: str | None,
        filter_criticity: str | None,
        page: int | None,
    ):
        view = build_paginated_view(
            snapshot=snapshot,
            source_key='tracking_items',
            search_text=search_text,
            sort_order_time=sort_order_time,
            filter_criticity=filter_criticity,
            page=page,
            page_size=ActiveAlarmsModalIds.PAGE_SIZE,
        )

        children = build_alarm_list_children(
            items=view['items'],
            panel_kind='tracking',
            page_size=ActiveAlarmsModalIds.PAGE_SIZE,
            has_snapshot=bool(view['has_snapshot']),
            empty_by_filter=bool(view['empty_by_filter']),
        )

        count_label = f'{view["total_items"]} {"Activa" if view["total_items"] == 1 else "Activas"}'
        page_text = f'Página {view["page"]} de {view["total_pages"]}'

        return (
            children,
            count_label,
            page_text,
            not view['has_previous'],
            not view['has_next'],
        )


def _build_last_updated_text(
    *,
    snapshot: dict[str, Any] | None,
) -> str:
    if not snapshot:
        return 'Sin actualización'

    source_display = snapshot.get('source_last_updated_display') or 'Sin fecha'
    captured_display = snapshot.get('captured_at_display') or 'Sin fecha'

    return f'Última actualización: {source_display} · Información obtenida: {captured_display}'


def _build_modal_content(*, runtime_store: dict | None) -> dict:
    snapshot = build_active_alarm_modal_snapshot(
        runtime_store=runtime_store,
    )

    return (True, snapshot, '', 'recent', 'all', _build_last_updated_text(snapshot=snapshot))
