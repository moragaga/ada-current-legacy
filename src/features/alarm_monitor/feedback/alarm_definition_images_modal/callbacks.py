from __future__ import annotations

from dash import ALL, Input, Output, State, ctx, html
from dash.exceptions import PreventUpdate

from src.app.dash import get_dash_app
from src.features.alarm_monitor.panel_distributed.ids import DistributedAlarmPanelIds
from src.features.configuration.admin_panels.alarm_management.images.services.alarm_image_runtime_query_service import (
    build_alarm_image_runtime_query_service,
)

from .components.runtime_image_gallery import (
    build_alarm_image_runtime_gallery,
)
from .ids import AlarmDefinitionImagesModalIds


def register_alarm_definition_images_modal_callbacks() -> None:
    app = get_dash_app()

    @app.callback(
        Output(
            component_id=AlarmDefinitionImagesModalIds.MODAL,
            component_property='is_open',
            allow_duplicate=True,
        ),
        Output(component_id=AlarmDefinitionImagesModalIds.TITLE, component_property='children'),
        Output(component_id=AlarmDefinitionImagesModalIds.BODY, component_property='children'),
        Input(
            component_id={
                'type': DistributedAlarmPanelIds.DEFINITION_ACTION,
                'alarm_name': ALL,
                'message_group_key': ALL,
                'modal_title': ALL,
            },
            component_property='n_clicks_timestamp',
        ),
        State(
            component_id={
                'type': DistributedAlarmPanelIds.DEFINITION_ACTION,
                'alarm_name': ALL,
                'message_group_key': ALL,
                'modal_title': ALL,
            },
            component_property='id',
        ),
        prevent_initial_call=True,
    )
    def toggle_alarm_definition_images_modal(
        definition_timestamps,
        definition_ids,
    ):
        triggered_id = ctx.triggered_id

        if triggered_id is None:
            raise PreventUpdate

        if not isinstance(triggered_id, dict):
            raise PreventUpdate

        if triggered_id.get('type') != DistributedAlarmPanelIds.DEFINITION_ACTION:
            raise PreventUpdate

        triggered_timestamp = _get_triggered_timestamp(
            triggered_id=triggered_id,
            timestamps=definition_timestamps or [],
            ids=definition_ids or [],
        )

        if triggered_timestamp <= 0:
            raise PreventUpdate

        alarm_name = str(triggered_id.get('alarm_name') or '').strip()
        message_group_key = str(triggered_id.get('message_group_key') or '').strip()
        modal_title = str(triggered_id.get('modal_title') or '').strip()

        if not message_group_key:
            return (
                True,
                modal_title or alarm_name or 'Imágenes de alarma',
                _build_missing_group_key_body(alarm_name=alarm_name),
            )

        image_group = build_alarm_image_runtime_query_service().get_images_for_message_group(
            message_group_key=message_group_key,
            sync_if_due=True,
        )

        title = modal_title or alarm_name or 'Imágenes de alarma'

        return (
            True,
            title,
            _build_modal_body(
                alarm_name=alarm_name,
                message_group_key=message_group_key,
                image_group=image_group,
            ),
        )

    @app.callback(
        Output(
            component_id=AlarmDefinitionImagesModalIds.MODAL,
            component_property='is_open',
            allow_duplicate=True,
        ),
        Input(
            component_id=AlarmDefinitionImagesModalIds.CLOSE_BUTTON, component_property='n_clicks'
        ),
        prevent_initial_call=True,
    )
    def close_modal(n_clicks: int | None):
        if n_clicks is not None or ctx.triggered_id == AlarmDefinitionImagesModalIds.CLOSE_BUTTON:
            return False

        raise PreventUpdate


def _build_modal_body(
    *,
    alarm_name: str,
    message_group_key: str,
    image_group,
) -> html.Div:
    return html.Div(
        className='alarm-definition-images-modal-content',
        children=build_alarm_image_runtime_gallery(
            image_group=image_group,
        ),
    )


def _build_missing_group_key_body(
    *,
    alarm_name: str,
) -> html.Div:
    return html.Div(
        className='alarm-definition-images-modal-empty',
        children=[
            html.Div(
                className='fw-semibold mb-1',
                children=alarm_name or 'Alarma sin grupo',
            ),
            html.Div(
                children='Esta alarma no tiene message_group_key asociado.',
            ),
        ],
    )


def _get_triggered_timestamp(
    *,
    triggered_id: dict,
    timestamps: list[int | None],
    ids: list[dict],
) -> int:
    for timestamp, current_id in zip(timestamps, ids, strict=False):
        if dict(current_id) == dict(triggered_id):
            try:
                return int(timestamp or -1)
            except Exception:
                return -1

    return -1
