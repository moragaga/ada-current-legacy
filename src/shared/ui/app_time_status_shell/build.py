from __future__ import annotations

from dash import html
from typing import TYPE_CHECKING

from dash.development.base_component import Component
if TYPE_CHECKING:
    from .model import AppTimeStatusShellGroupStructure, AppTimeStatusShellStructure


def build_time_status_indicator(
    *,
    definition: AppTimeStatusShellStructure
) -> Component:
    if definition.value is None:
        value = ''
    else:
        value = definition.value
    return html.Span(
        className='d-flex fs-io-hi-200',
        children=[
            html.Span(
                className=f'd-flex gap-1 {definition.wrapper_class_name or ""}',
                children=[
                    html.I(id=definition.icon_id or '', className=f'{definition.icon_class_name} item-value'),
                    html.P(className='item-value', children=[definition.label]),
                    html.P(className='item-value', children=['•']),
                    html.P(id=definition.value_id or '', className='time-value time-window-value', children=[value]),
                ]
            ),
            html.Span(className='px-1 fw-lighter', children=['|']) if definition.right_divisor else None,
        ]
    )

def build_time_status_indicator_group(
    *,
    definitions: AppTimeStatusShellGroupStructure
) -> Component:
    return html.Div(
        className='d-flex',
        children=[build_time_status_indicator(definition=definition) for definition in definitions],
    )