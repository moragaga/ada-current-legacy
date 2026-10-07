from __future__ import annotations

from typing import Any

import dash_bootstrap_components as dbc
from dash import html
from dash.development.base_component import Component

from .primitives import build_colgroup, build_table_body, build_table_header
from ...display.error_component import build_error_component

TABLE_WRAPPER_CLASS_NAME = 'compact-table-wrapper'
TABLE_CLASS_NAME = 'compact-table'


def build_compact_table_replacement_component(
    *,
    value: Any,
) -> Component:
    if isinstance(value, Component):
        return value

    return html.Div(
        children=[
            build_error_component()
        ] if value is None else [value],
    )


def build_compact_table_component(
    *,
    columns: tuple[Any, ...],
    rows: tuple[Any, ...],
    show_header: bool = True,
    class_name: str = '',
    wrapper_class_name: str = '',
    emphasized: bool = True,
) -> Component:
    table_children: list[Component] = []

    colgroup = build_colgroup(
        columns=columns,
    )
    if colgroup is not None:
        table_children.append(colgroup)

    if show_header:
        table_children.append(
            build_table_header(
                columns=columns,
                emphasized=emphasized,
            ),
        )

    table_children.append(
        build_table_body(
            columns=columns,
            rows=rows,
        ),
    )

    return html.Div(
        className=f'{TABLE_WRAPPER_CLASS_NAME} {wrapper_class_name}'.strip(),
        children=[
            dbc.Table(
                className=f'm-0 table-borderless {TABLE_CLASS_NAME} {class_name}'.strip(),
                children=table_children,
            ),
        ],
    )
