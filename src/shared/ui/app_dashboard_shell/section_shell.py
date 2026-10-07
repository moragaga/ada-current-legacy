from __future__ import annotations

import dash_bootstrap_components as dbc
from dash import html


def build_section_shell(
    *,
    title: str,
    content_id: str,
    children=None,
    external_links_component=None,
    wrapper_class_name: str = 'p-0 d-flex flex-column h-100',
    title_wrapper_class_name: str = 'd-flex justify-content-center align-items-center',
    title_text_class_name: str = 'text-center text-white component-master-title',
    content_wrapper_class_name: str = 'd-flex flex-column gap-1 h-100',
) -> dbc.Container:
    children = children or []

    header_children = [html.P(className=title_text_class_name, children=[title])]

    if external_links_component is not None:
        header_children.append(external_links_component)

    return dbc.Container(
        id=content_id,
        className=wrapper_class_name,
        fluid=True,
        children=[
            html.Div(className=title_wrapper_class_name, children=header_children),
            html.Div(className=content_wrapper_class_name, children=children),
        ],
    )
