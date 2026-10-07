from __future__ import annotations

from typing import Any

from dash import Input, Output, State, ctx
from dash.exceptions import PreventUpdate

from src.app.dash import get_dash_app
from src.features.alarm_monitor.feedback.managed_alarms_modal.constants import (
    DEFAULT_CRITICITY_FILTER,
    DEFAULT_RECURRENCE_MIN_DURATION,
    DEFAULT_SORT_ORDER,
    DEFAULT_STATUS_FILTER,
    ITEMS_CONTENT_SIDE_HIDE_CLASSNAME,
    ITEMS_CONTENT_SIDE_SHOW_CLASSNAME,
    ZOOM_IN_CONTENT_MAIN_BUTTON_CLASSNAME,
    ZOOM_OUT_CONTENT_MAIN_BUTTON_CLASSNAME,
)
from src.features.basic_analytics_runtime.managed_alarms.services import (
    get_managed_alarm_analytics_runtime_service,
)

from .components import (
    build_managed_alarm_list_children,
    build_summary_cards,
)
from .graphs import (
    build_recurrence_figure,
)
from .ids import (
    ManagedAlarmsModalIds,
)
from .services import (
    build_managed_alarm_modal_snapshot,
    build_paginated_view,
    get_next_page,
    get_total_pages_for_items,
    get_turn_scope_options,
    resolve_default_turn_scope_filter,
)


def register_managed_alarms_modal_callbacks() -> None:
    app = get_dash_app()

    @app.callback(
        Output(
            component_id=ManagedAlarmsModalIds.MODAL,
            component_property='is_open',
            allow_duplicate=True,
        ),
        Output(
            component_id=ManagedAlarmsModalIds.FROZEN_SNAPSHOT_STORE,
            component_property='data',
            allow_duplicate=True,
        ),
        Output(
            component_id=ManagedAlarmsModalIds.SEARCH_INPUT,
            component_property='value',
            allow_duplicate=True,
        ),
        Output(
            component_id=ManagedAlarmsModalIds.SORT_SELECT_TIME,
            component_property='value',
            allow_duplicate=True,
        ),
        Output(
            component_id=ManagedAlarmsModalIds.FILTER_SELECT_CRITICITY,
            component_property='value',
            allow_duplicate=True,
        ),
        Output(
            component_id=ManagedAlarmsModalIds.FILTER_SELECT_STATUS,
            component_property='value',
            allow_duplicate=True,
        ),
        Output(
            component_id=ManagedAlarmsModalIds.FILTER_SELECT_TURN_SCOPE,
            component_property='value',
            allow_duplicate=True,
        ),
        Output(
            component_id=ManagedAlarmsModalIds.FILTER_SELECT_TURN_SCOPE,
            component_property='options',
            allow_duplicate=True,
        ),
        Output(
            component_id=ManagedAlarmsModalIds.RECURRENCE_MIN_DURATION_SELECT,
            component_property='value',
            allow_duplicate=True,
        ),
        Output(
            component_id=ManagedAlarmsModalIds.LAST_UPDATED_TEXT,
            component_property='children',
            allow_duplicate=True,
        ),
        Input(component_id=ManagedAlarmsModalIds.OPEN_BUTTON, component_property='n_clicks'),
        State(component_id=ManagedAlarmsModalIds.MODAL, component_property='is_open'),
        prevent_initial_call=True,
    )
    def open_modal(
        n_clicks: int | None,
        is_open: bool,
    ):
        if (
            ctx.triggered_id is None
            or n_clicks is None
            or not n_clicks
            or is_open
            or ctx.triggered_id != ManagedAlarmsModalIds.OPEN_BUTTON
        ):
            raise PreventUpdate

        return _build_modal_content()

    @app.callback(
        Output(
            component_id=ManagedAlarmsModalIds.MODAL,
            component_property='is_open',
            allow_duplicate=True,
        ),
        Output(
            component_id=ManagedAlarmsModalIds.FROZEN_SNAPSHOT_STORE,
            component_property='data',
            allow_duplicate=True,
        ),
        Output(
            component_id=ManagedAlarmsModalIds.SEARCH_INPUT,
            component_property='value',
            allow_duplicate=True,
        ),
        Output(
            component_id=ManagedAlarmsModalIds.SORT_SELECT_TIME,
            component_property='value',
            allow_duplicate=True,
        ),
        Output(
            component_id=ManagedAlarmsModalIds.FILTER_SELECT_CRITICITY,
            component_property='value',
            allow_duplicate=True,
        ),
        Output(
            component_id=ManagedAlarmsModalIds.FILTER_SELECT_STATUS,
            component_property='value',
            allow_duplicate=True,
        ),
        Output(
            component_id=ManagedAlarmsModalIds.FILTER_SELECT_TURN_SCOPE,
            component_property='value',
            allow_duplicate=True,
        ),
        Output(
            component_id=ManagedAlarmsModalIds.FILTER_SELECT_TURN_SCOPE,
            component_property='options',
            allow_duplicate=True,
        ),
        Output(
            component_id=ManagedAlarmsModalIds.RECURRENCE_MIN_DURATION_SELECT,
            component_property='value',
            allow_duplicate=True,
        ),
        Output(
            component_id=ManagedAlarmsModalIds.LAST_UPDATED_TEXT,
            component_property='children',
            allow_duplicate=True,
        ),
        Input(component_id=ManagedAlarmsModalIds.REFRESH_BUTTON, component_property='n_clicks'),
        State(component_id=ManagedAlarmsModalIds.MODAL, component_property='is_open'),
        prevent_initial_call=True,
    )
    def refresh_modal(
        n_clicks: int | None,
        is_open: bool,
    ):
        if (
            ctx.triggered_id is None
            or n_clicks is None
            or not is_open
            or not n_clicks
            or ctx.triggered_id != ManagedAlarmsModalIds.REFRESH_BUTTON
        ):
            raise PreventUpdate

        return _build_modal_content()

    @app.callback(
        Output(
            component_id=ManagedAlarmsModalIds.MODAL,
            component_property='is_open',
            allow_duplicate=True,
        ),
        Input(component_id=ManagedAlarmsModalIds.CLOSE_BUTTON, component_property='n_clicks'),
        prevent_initial_call=True,
    )
    def close_modal(
        n_clicks: int | None,
    ):
        if n_clicks is not None and ctx.triggered_id == ManagedAlarmsModalIds.CLOSE_BUTTON:
            return False

        raise PreventUpdate

    @app.callback(
        Output(component_id=ManagedAlarmsModalIds.ITEMS_PAGE_STORE, component_property='data'),
        Input(
            component_id=ManagedAlarmsModalIds.ITEMS_PREVIOUS_BUTTON, component_property='n_clicks'
        ),
        Input(component_id=ManagedAlarmsModalIds.ITEMS_NEXT_BUTTON, component_property='n_clicks'),
        Input(component_id=ManagedAlarmsModalIds.SEARCH_INPUT, component_property='value'),
        Input(component_id=ManagedAlarmsModalIds.SORT_SELECT_TIME, component_property='value'),
        Input(
            component_id=ManagedAlarmsModalIds.FILTER_SELECT_CRITICITY, component_property='value'
        ),
        Input(component_id=ManagedAlarmsModalIds.FILTER_SELECT_STATUS, component_property='value'),
        Input(
            component_id=ManagedAlarmsModalIds.FILTER_SELECT_TURN_SCOPE, component_property='value'
        ),
        Input(component_id=ManagedAlarmsModalIds.FROZEN_SNAPSHOT_STORE, component_property='data'),
        State(component_id=ManagedAlarmsModalIds.ITEMS_PAGE_STORE, component_property='data'),
    )
    def update_items_page(
        previous_clicks: int | None,
        next_clicks: int | None,
        search_text: str | None,
        sort_order_time: str | None,
        filter_criticity: str | None,
        filter_status: str | None,
        filter_turn_scope: str | None,
        snapshot: dict[str, Any] | None,
        current_page: int | None,
    ):
        triggered_id = ctx.triggered_id

        if triggered_id in {
            ManagedAlarmsModalIds.SEARCH_INPUT,
            ManagedAlarmsModalIds.SORT_SELECT_TIME,
            ManagedAlarmsModalIds.FILTER_SELECT_CRITICITY,
            ManagedAlarmsModalIds.FILTER_SELECT_STATUS,
            ManagedAlarmsModalIds.FILTER_SELECT_TURN_SCOPE,
            ManagedAlarmsModalIds.FROZEN_SNAPSHOT_STORE,
        }:
            return 1

        total_pages = get_total_pages_for_items(
            snapshot=snapshot,
            search_text=search_text,
            sort_order_time=sort_order_time,
            filter_criticity=filter_criticity,
            filter_status=filter_status,
            filter_turn_scope=filter_turn_scope,
            page_size=ManagedAlarmsModalIds.PAGE_SIZE,
        )

        if triggered_id == ManagedAlarmsModalIds.ITEMS_PREVIOUS_BUTTON:
            return get_next_page(
                current_page=current_page,
                direction='previous',
                total_pages=total_pages,
            )

        if triggered_id == ManagedAlarmsModalIds.ITEMS_NEXT_BUTTON:
            return get_next_page(
                current_page=current_page,
                direction='next',
                total_pages=total_pages,
            )

        return current_page or 1

    @app.callback(
        Output(component_id=ManagedAlarmsModalIds.SUMMARY_CONTAINER, component_property='children'),
        Output(component_id=ManagedAlarmsModalIds.RECURRENCE_CHART, component_property='figure'),
        Output(component_id=ManagedAlarmsModalIds.ITEMS_LIST, component_property='children'),
        Output(component_id=ManagedAlarmsModalIds.ITEMS_COUNT, component_property='children'),
        Output(component_id=ManagedAlarmsModalIds.ITEMS_PAGE_TEXT, component_property='children'),
        Output(
            component_id=ManagedAlarmsModalIds.ITEMS_PREVIOUS_BUTTON, component_property='disabled'
        ),
        Output(component_id=ManagedAlarmsModalIds.ITEMS_NEXT_BUTTON, component_property='disabled'),
        Input(component_id=ManagedAlarmsModalIds.FROZEN_SNAPSHOT_STORE, component_property='data'),
        Input(component_id=ManagedAlarmsModalIds.SEARCH_INPUT, component_property='value'),
        Input(component_id=ManagedAlarmsModalIds.SORT_SELECT_TIME, component_property='value'),
        Input(
            component_id=ManagedAlarmsModalIds.FILTER_SELECT_CRITICITY, component_property='value'
        ),
        Input(component_id=ManagedAlarmsModalIds.FILTER_SELECT_STATUS, component_property='value'),
        Input(
            component_id=ManagedAlarmsModalIds.FILTER_SELECT_TURN_SCOPE, component_property='value'
        ),
        Input(
            component_id=ManagedAlarmsModalIds.RECURRENCE_MIN_DURATION_SELECT,
            component_property='value',
        ),
        Input(component_id=ManagedAlarmsModalIds.ITEMS_PAGE_STORE, component_property='data'),
    )
    def render_modal_content(
        snapshot: dict[str, Any] | None,
        search_text: str | None,
        sort_order_time: str | None,
        filter_criticity: str | None,
        filter_status: str | None,
        filter_turn_scope: str | None,
        recurrence_min_duration: str | None,
        page: int | None,
    ):
        view = build_paginated_view(
            snapshot=snapshot,
            search_text=search_text,
            sort_order_time=sort_order_time,
            filter_criticity=filter_criticity,
            filter_status=filter_status,
            filter_turn_scope=filter_turn_scope,
            page=page,
            page_size=ManagedAlarmsModalIds.PAGE_SIZE,
        )

        list_children = build_managed_alarm_list_children(
            items=view['items'],
            page_size=ManagedAlarmsModalIds.PAGE_SIZE,
            has_snapshot=bool(view['has_snapshot']),
            empty_by_filter=bool(view['empty_by_filter']),
        )

        total_items = int(view['total_items'])
        count_label = f'{total_items} gestión' if total_items == 1 else f'{total_items} gestiones'

        page_text = f'Página {view["page"]} de {view["total_pages"]}'

        return (
            build_summary_cards(
                snapshot=snapshot,
                turn_scope_filter=filter_turn_scope,
            ),
            build_recurrence_figure(
                snapshot=snapshot,
                min_duration=recurrence_min_duration,
                turn_scope_filter=filter_turn_scope,
            ),
            list_children,
            count_label,
            page_text,
            not view['has_previous'],
            not view['has_next'],
        )

    @app.callback(
        Output(
            component_id=ManagedAlarmsModalIds.ZOOM_MAIN_CONTENT_BUTTON,
            component_property='className',
        ),
        Output(
            component_id=ManagedAlarmsModalIds.ITEMS_SIDE_CONTENT, component_property='className'
        ),
        Input(
            component_id=ManagedAlarmsModalIds.ZOOM_MAIN_CONTENT_BUTTON,
            component_property='n_clicks',
        ),
        State(
            component_id=ManagedAlarmsModalIds.ITEMS_SIDE_CONTENT, component_property='className'
        ),
        prevent_initial_call=True,
    )
    def zoom_main_content(n_clicks, class_name):
        if n_clicks is None or ctx.triggered_id is None:
            raise PreventUpdate

        if class_name.strip() == 'd-none':
            return ZOOM_IN_CONTENT_MAIN_BUTTON_CLASSNAME, ITEMS_CONTENT_SIDE_SHOW_CLASSNAME
        return ZOOM_OUT_CONTENT_MAIN_BUTTON_CLASSNAME, ITEMS_CONTENT_SIDE_HIDE_CLASSNAME


def _build_modal_content() -> tuple:
    analytics_snapshot = get_managed_alarm_analytics_runtime_service().get_snapshot()

    snapshot = build_managed_alarm_modal_snapshot(
        analytics_snapshot=analytics_snapshot,
    )

    turn_scope_options = get_turn_scope_options()
    default_turn_scope_filter = resolve_default_turn_scope_filter()

    return (
        True,
        snapshot,
        '',
        DEFAULT_SORT_ORDER,
        DEFAULT_CRITICITY_FILTER,
        DEFAULT_STATUS_FILTER,
        default_turn_scope_filter,
        turn_scope_options,
        DEFAULT_RECURRENCE_MIN_DURATION,
        _build_last_updated_text(snapshot=snapshot),
    )


def _build_last_updated_text(
    *,
    snapshot: dict[str, Any] | None,
) -> str:
    if not snapshot:
        return 'Sin actualización'

    source_display = snapshot.get('source_snapshot_timestamp_display') or 'Sin fecha'
    captured_display = snapshot.get('captured_at_display') or 'Sin fecha'

    return f'Última actualización: {source_display} · Información obtenida: {captured_display}'
