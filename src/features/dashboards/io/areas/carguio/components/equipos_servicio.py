from __future__ import annotations

from typing import Any
from dash import html
from dash.development.base_component import Component


def build_equipos_servicio_table_component(*, data: dict[str, Any]) -> Component:
    items = data.get('rows', [])
    total_data = data.get('total')

    rows = [
        _build_row(
            label=item['label'],
            op_real=item['op_real'],
            op_plan=item['op_plan'],
            disp_real=item['disp_real'],
            disp_plan=item['disp_plan'],
            fs_real=item['fs_real'],
            fs_plan=item['fs_plan'],
            op_color=item.get('op_color'),
            is_last=(index == len(items) - 1),
        )
        for index, item in enumerate(items)
    ]

    if total_data:
        rows.append(
            _build_row(
                label=total_data['label'],
                op_real=total_data['op_real'],
                op_plan=total_data['op_plan'],
                disp_real=total_data['disp_real'],
                disp_plan=total_data['disp_plan'],
                fs_real=total_data['fs_real'],
                fs_plan=total_data['fs_plan'],
                is_total=True,
                is_last=True,
            )
        )

    return html.Div(
        className='w-100',
        style={'padding': '0 4px', 'boxSizing': 'border-box'},
        children=[
            # Encabezado (OP / DISP / F.S.) simétrico con 3 columnas
            html.Div(
                style={
                    'display': 'grid',
                    'gridTemplateColumns': 'repeat(3, minmax(0, 1fr))',
                    'width': '100%',
                    'borderBottom': '1px solid #c0c0c0',
                    'paddingBottom': '4px',
                    'marginBottom': '1px',
                },
                children=[
                    html.Div(
                        style={
                            'minWidth': '0',
                            'display': 'flex',
                            'flexDirection': 'column',
                            'alignItems': 'center',
                            'justifyContent': 'center',
                            'textAlign': 'center',
                        },
                        children=[
                            html.Div(
                                'Operando',
                                style={
                                    'fontWeight': '700',
                                    'fontSize': 'clamp(7px, 0.9vw, 8px)',
                                    'color': '#515151',
                                    'letterSpacing': '0.3px',
                                    'lineHeight': '1.2',
                                    'whiteSpace': 'nowrap',
                                },
                            ),
                            html.Div(
                                'Operando',
                                style={
                                    'fontSize': 'clamp(5.8px, 0.75vw, 7px)',
                                    'color': '#555555',
                                    'whiteSpace': 'nowrap',
                                    'lineHeight': '1.2',
                                    'marginTop': '1px',
                                },
                            ),
                        ],
                    ),
                    html.Div(
                        style={
                            'minWidth': '0',
                            'display': 'flex',
                            'flexDirection': 'column',
                            'alignItems': 'center',
                            'justifyContent': 'center',
                            'textAlign': 'center',
                        },
                        children=[
                            html.Div(
                                'Disponibles',
                                style={
                                    'fontWeight': '700',
                                    'fontSize': 'clamp(7px, 0.9vw, 8px)',
                                    'color': '#515151',
                                    'letterSpacing': '0.3px',
                                    'lineHeight': '1.2',
                                    'whiteSpace': 'nowrap',
                                },
                            ),
                            html.Div(
                                'Disponible',
                                style={
                                    'fontSize': 'clamp(5.8px, 0.75vw, 7px)',
                                    'color': '#555555',
                                    'whiteSpace': 'nowrap',
                                    'lineHeight': '1.2',
                                    'marginTop': '1px',
                                },
                            ),
                        ],
                    ),
                    html.Div(
                        style={
                            'minWidth': '0',
                            'display': 'flex',
                            'flexDirection': 'column',
                            'alignItems': 'center',
                            'justifyContent': 'center',
                            'textAlign': 'center',
                        },
                        children=[
                            html.Div(
                                'Fuera de servicio.',
                                style={
                                    'fontWeight': '700',
                                    'fontSize': 'clamp(7px, 0.9vw, 8px)',
                                    'color': '#515151',
                                    'letterSpacing': '0.3px',
                                    'lineHeight': '1.2',
                                    'whiteSpace': 'nowrap',
                                },
                            ),
                            html.Div(
                                'Fuera Serv.',
                                style={
                                    'fontSize': 'clamp(5.8px, 0.75vw, 7px)',
                                    'color': '#555555',
                                    'whiteSpace': 'nowrap',
                                    'lineHeight': '1.2',
                                    'marginTop': '1px',
                                },
                            ),
                        ],
                    ),
                ],
            ),
            # Filas de datos
            html.Div(children=rows),
        ],
    )


def _build_row(
    *,
    label: str,
    op_real: str | int | float = '-',
    op_plan: str | int | float = '-',
    disp_real: str | int | float = '-',
    disp_plan: str | int | float = '-',
    fs_real: str | int | float = '-',
    fs_plan: str | int | float = '-',
    op_color: str | None = None,
    is_total: bool = False,
    is_last: bool = False,
) -> Component:
    if is_total:
        border_style = {
            'borderTop': '1.5px solid #808080',
            'borderBottom': 'none',
            'paddingTop': '5px',
            'paddingBottom': '4px',
            'marginTop': '2px',
        }
    else:
        border_style = {
            'borderBottom': 'none' if is_last else '1px solid #d0d0d0',
            'paddingTop': '3.5px',
            'paddingBottom': '3.5px',
        }

    return html.Div(
        style={'width': '100%', **border_style},
        children=[
            # Etiqueta
            html.Div(
                label,
                style={
                    'fontSize': 'clamp(6.8px, 0.85vw, 8px)' if is_total else 'clamp(6.5px, 0.8vw, 7.5px)',
                    'fontWeight': '800' if is_total else '600',
                    'color': '#212529' if is_total else '#4a4a4a',
                    'lineHeight': '1.2',
                    'marginBottom': '2px',
                    'paddingLeft': '2px',
                    'whiteSpace': 'nowrap',
                },
            ),
            # 3 Columnas simétricas
            html.Div(
                style={
                    'display': 'grid',
                    'gridTemplateColumns': 'repeat(3, minmax(0, 1fr))',
                    'width': '100%',
                    'alignItems': 'baseline',
                },
                children=[
                    # OP
                    html.Div(
                        style={
                            'minWidth': '0',
                            'display': 'flex',
                            'justifyContent': 'center',
                            'alignItems': 'baseline',
                            'gap': '2px',
                            'whiteSpace': 'nowrap',
                        },
                        children=[
                            html.Span(
                                f'{op_real}',
                                style={
                                    'fontWeight': '700',
                                    'fontSize': 'clamp(7.5px, 0.95vw, 8.5px)',
                                    'color': op_color if (op_color and not is_total) else '#515151',
                                    'lineHeight': '1.2',
                                },
                            ),
                            html.Span(
                                f'/ {op_plan}',
                                style={
                                    'fontSize': 'clamp(6.5px, 0.8vw, 7.5px)',
                                    'color': '#595959',
                                    'lineHeight': '1.2',
                                },
                            ),
                        ],
                    ),
                    # DISP
                    html.Div(
                        style={
                            'minWidth': '0',
                            'display': 'flex',
                            'justifyContent': 'center',
                            'alignItems': 'baseline',
                            'gap': '2px',
                            'whiteSpace': 'nowrap',
                        },
                        children=[
                            html.Span(
                                f'{disp_real}',
                                style={
                                    'fontWeight': '700',
                                    'fontSize': 'clamp(7.5px, 0.95vw, 8.5px)',
                                    'color': '#515151',
                                    'lineHeight': '1.2',
                                },
                            ),
                            html.Span(
                                f'/ {disp_plan}',
                                style={
                                    'fontSize': 'clamp(6.5px, 0.8vw, 7.5px)',
                                    'color': '#595959',
                                    'lineHeight': '1.2',
                                },
                            ),
                        ],
                    ),
                    # F.S.
                    html.Div(
                        style={
                            'minWidth': '0',
                            'display': 'flex',
                            'justifyContent': 'center',
                            'alignItems': 'baseline',
                            'gap': '2px',
                            'whiteSpace': 'nowrap',
                        },
                        children=[
                            html.Span(
                                f'{fs_real}',
                                style={
                                    'fontWeight': '700',
                                    'fontSize': 'clamp(7.5px, 0.95vw, 8.5px)',
                                    'color': '#515151',
                                    'lineHeight': '1.2',
                                },
                            ),
                            html.Span(
                                f'/ {fs_plan}',
                                style={
                                    'fontSize': 'clamp(6.5px, 0.8vw, 7.5px)',
                                    'color': '#595959',
                                    'lineHeight': '1.2',
                                },
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )


def build_equipos_servicio_total_component(*, total_values: tuple[str, str] = ('', '')) -> Component:
    return html.Div()