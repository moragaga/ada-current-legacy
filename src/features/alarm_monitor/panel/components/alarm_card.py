from __future__ import annotations

import dash_bootstrap_components as dbc
from dash import html

from src.features.alarm_management.operator.components import (
    build_alarm_management_button,
)
from src.shared.ui.theme import resolve_color_class

from ..ids import AlarmPanelIds
from ..models.alarm_card_view_definition import AlarmCardViewDefinition


def build_alarm_card(
    *,
    alarm: AlarmCardViewDefinition,
):
    background_color = resolve_color_class(
        value=alarm.color,
        type_color='background',
    )
    border_color = resolve_color_class(
        value=alarm.color,
        type_color='border',
    )

    return dbc.Card(
        className=f'alarm-panel-card {border_color}',
        children=[
            dbc.CardHeader(
                className=(f'd-flex justify-content-between {background_color} px-2 py-1'),
                children=[
                    html.I(
                        id={
                            'type': AlarmPanelIds.DEFINITION_ACTION,
                            'alarm_name': alarm.alarm_name,
                            'message_group_key': alarm.message_group_key,
                            'modal_title': alarm.modal_title,
                        },
                        className='bi bi-info-circle-fill active-cursor text-white d-flex align-items-center',
                        n_clicks=0,
                    ),
                    html.Span(
                        className='fw-semibold text-white d-flex align-items-center',
                        children=[alarm.alarm_kind],
                    ),
                    build_alarm_management_button(
                        alarm_id=alarm.alarm_id,
                        group_occurrence_id=alarm.group_occurrence_id,
                        alarm_key=alarm.alarm_key,
                        visibility_group_key=alarm.visibility_group_key,
                        management_scope_key=alarm.management_scope_key,
                        priority_order=alarm.priority_order,
                        target_occurrence_started_at=alarm.target_occurrence_started_at,
                        allow_management=alarm.is_show_delete,
                    ),
                ],
            ),
            dbc.CardBody(
                className='alarm-panel-card-body background-primary p-0',
                children=[
                    html.Div(
                        className='title',
                        children=[alarm.title],
                    ),
                    html.Div(
                        className='description',
                        children=[
                            html.Div(
                                className='cause',
                                children=[line],
                            )
                            for line in alarm.cause_lines
                        ],
                    ),
                ],
            ),
            dbc.CardFooter(
                className='px-2 py-0 text-start background-primary',
                children=[
                    'Activa por:\u00a0',
                    html.Strong(children=[alarm.activity_time]),
                ],
            ),
        ],
    )
