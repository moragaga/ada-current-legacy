from __future__ import annotations

from dash import html


def build_navigation_offcanvas_title() -> html.Div:
    return html.Div(
        className='app-navigation-offcanvas-title',
        children=[
            html.Div(
                className='app-navigation-offcanvas-title-icon',
                children=[
                    html.I(className='bi bi-app-indicator'),
                ],
            ),
            html.Div(
                className='app-navigation-offcanvas-title-text',
                children=[
                    html.H5(
                        className='app-navigation-offcanvas-title-heading',
                        children='ADA N1',
                    ),
                    html.P(
                        className='app-navigation-offcanvas-title-subtitle',
                        children='Navegación del proyecto',
                    ),
                ],
            ),
        ],
    )
