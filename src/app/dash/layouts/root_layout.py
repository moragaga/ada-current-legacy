from __future__ import annotations

from dash import dcc, html, page_container


class RootLayout:
    @staticmethod
    def render(version: str):
        return html.Div(
            children=[
                dcc.Location(id='url', refresh=False),
                html.Div(
                    id='page-content',
                    children=[
                        page_container,
                    ],
                ),
                html.Span(className='d-none', children=[version]),
            ]
        )
