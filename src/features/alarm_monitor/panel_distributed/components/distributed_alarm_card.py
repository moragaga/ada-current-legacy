from __future__ import annotations

import dash_bootstrap_components as dbc
from dash import html
from dash.development.base_component import Component

from src.features.alarm_management.distributed_operator.components import (
    build_distributed_alarm_bulk_management_button,
    build_distributed_alarm_management_button,
)
from src.shared.ui.theme import resolve_color_class

from ..ids import DistributedAlarmPanelIds
from ..models.distributed_alarm_bulk_group_view_definition import (
    DistributedAlarmBulkGroupViewDefinition,
)
from ..models.distributed_alarm_card_view_definition import (
    DistributedAlarmCardViewDefinition,
)


def build_distributed_alarm_card(
    *,
    alarm: DistributedAlarmCardViewDefinition,
    bulk_group: DistributedAlarmBulkGroupViewDefinition | None = None,
) -> Component:
    background_color = resolve_color_class(
        value=alarm.color,
        type_color='background',
    )
    border_color = resolve_color_class(
        value=alarm.color,
        type_color='border',
    )

    information, is_merge = _build_information(
        alarm=alarm,
        bulk_group=bulk_group,
    )

    if is_merge:
        information = [
            html.Div(
                className='d-flex align-items-center justify-content-center gap-1',
                children=information,
            )
        ]

    return dbc.Card(
        className=f'alarm-panel-card {border_color}',
        children=[
            dbc.CardHeader(
                className=(
                    f'd-flex justify-content-between align-items-center {background_color} px-2'
                ),
                children=[
                    _build_bulk_badge(
                        alarm=alarm,
                        bulk_group=bulk_group,
                        allow_management=alarm.is_show_delete,
                    ),
                    *information,
                    build_distributed_alarm_management_button(
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
                    html.Strong(children=alarm.activity_time),
                ],
            ),
        ],
    )


def _build_bulk_badge(
    *,
    alarm: DistributedAlarmCardViewDefinition,
    bulk_group: DistributedAlarmBulkGroupViewDefinition | None,
    allow_management: bool,
) -> Component:
    if bulk_group is None or not allow_management or bulk_group.anchor_alarm_id != alarm.alarm_id:
        return html.Span()

    return build_distributed_alarm_bulk_management_button(
        group_key=bulk_group.key,
        group_label=bulk_group.label,
        alarm_items=bulk_group.items,
        count=bulk_group.count,
        icon_class_name=bulk_group.icon_class_name,
    )


def _build_information(
    alarm: DistributedAlarmCardViewDefinition,
    bulk_group: DistributedAlarmBulkGroupViewDefinition | None,
) -> tuple[list[Component], bool]:
    is_h2s = bool(bulk_group and alarm.operator_bucket.strip() == 'h2s')
    class_name_definition = '' if is_h2s else 'me-auto'
    class_name_kind = '' if is_h2s else 'mx-auto'

    information = [
        html.Span(
            className='d-flex align-items-center',
            children=[
                html.Button(
                    id={
                        'type': DistributedAlarmPanelIds.DEFINITION_ACTION,
                        'alarm_name': alarm.alarm_name,
                        'message_group_key': alarm.message_group_key,
                        'modal_title': alarm.modal_title,
                    },
                    className='alarm-definition-action-button',
                    children=[
                        html.I(
                            className=(
                                'bi bi-info-circle-fill active-cursor text-white '
                                f'{class_name_definition}'
                            ).strip(),
                        ),
                    ],
                    type='button',
                )
            ],
        ),
        html.Span(
            className=(
                f'fw-semibold text-white d-flex align-items-center {class_name_kind}'
            ).strip(),
            children=[alarm.alarm_kind],
        ),
    ]

    return information, is_h2s
