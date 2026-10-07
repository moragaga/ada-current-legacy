from __future__ import annotations

import dash_bootstrap_components as dbc
from dash import html


def build_toast(
    *,
    header: str,
    message: str | list[str] | html.Div | html.Ul,
    icon: str = 'primary',
) -> dbc.Toast:
    content = message

    if isinstance(message, list):
        content = html.Ul(
            [html.Li(item) for item in message[:8]],
            className='mb-0 ps-3',
        )

    return dbc.Toast(
        header=header,
        children=content,
        icon=icon,
        duration=5000,
        dismissable=True,
        is_open=True,
        style={
            'position': 'fixed',
            'top': 66,
            'right': 10,
            'width': 420,
            'zIndex': 2000,
        },
    )
