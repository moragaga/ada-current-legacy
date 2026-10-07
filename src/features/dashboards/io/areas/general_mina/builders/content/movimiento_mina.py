from __future__ import annotations

import math
from typing import Any

from dash import html


def _to_float(val: Any) -> float | None:
    if val is None:
        return None
    if isinstance(val, (int, float)):
        return None if math.isnan(val) else float(val)
    val_str = str(val).replace('*', '').replace(',', '.').strip()
    if val_str in ('', '-', '--', 'nan', 'NaN', 'None', 'null'):
        return None
    try:
        f = float(val_str)
        return None if math.isnan(f) else f
    except (ValueError, TypeError):
        return None


def _resolve_metric_color(actual: Any, target: Any) -> str:
    """Aplica color directo:

    - Si actual >= target: No se pinta (gris '#4a4a4a').
    - Si déficit <= 3%: Amarillo ('#d4ac0d').
    - Si déficit > 3%: Rojo ('#d93829').
    """
    act = _to_float(actual)
    tgt = _to_float(target)

    # Si no hay datos válidos o el plan es 0/negativo, mantener gris base
    if act is None or tgt is None or tgt <= 0:
        return '#4a4a4a'

    # Si el valor real es mayor o igual al plan, no se pinta
    if act >= tgt:
        return '#4a4a4a'

    deficit_ratio = (tgt - act) / tgt
    if deficit_ratio <= 0.03:
        return '#d4ac0d'  # Amarillo visible en fondo claro
    return '#d93829'      # Rojo para déficit superior al 3%


def build_movimiento_mina_content(kpis: dict):
    movimiento_mina_summary = kpis.get('movimiento_mina_summary_inst', {})

    labels = [
        'Ext. Mina Total',
        'Remanejo',
        'Mov. Mina Total',
        'F9',
        'F10',
        'F11',
        'F12',
    ]
    keys = [
        'extraccion_mina',
        'remanejo',
        'movimiento_mina',
        'fase_9',
        'fase_10',
        'fase_11',
        'fase_12',
    ]

    if not movimiento_mina_summary.get('is_ok'):
        default_value = movimiento_mina_summary.get('default', '-')
        data = {
            key: dict.fromkeys(
                ['real', 'plan', 'proyeccion', 'objetivo_dia', 'requerido'],
                default_value,
            )
            for key in keys
        }
    else:
        _data = movimiento_mina_summary.get('payload', [])
        data = {}
        for item in _data:
            item_copy = item.copy()
            _key = item_copy.pop('key', None)
            item_copy.pop('label', None)
            if _key:
                data[_key] = item_copy

    rows = []
    for index, label in enumerate(labels):
        _key = keys[index]
        data_tmp = data.get(_key, {})
        rows.append(
            build_row(
                label=label,
                index=index,
                **data_tmp,
            )
        )

    return html.Div(
        className='w-100',
        style={'padding': '0 4px', 'boxSizing': 'border-box'},
        children=[
            # Encabezado (AVANCE / CIERRE / RITMO)
            html.Div(
                style={
                    'display': 'grid',
                    'gridTemplateColumns': 'repeat(3, minmax(0, 1fr))',
                    'width': '100%',
                    'borderBottom': '1px solid #c4c4c4',
                    'paddingBottom': '2px',
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
                                'AVANCE',
                                style={
                                    'fontWeight': '700',
                                    'fontSize': 'clamp(5.5px, 0.65vw, 6.5px)',
                                    'color': '#4a4a4a',
                                    'letterSpacing': '0.2px',
                                    'lineHeight': '1.1',
                                    'whiteSpace': 'nowrap',
                                },
                            ),
                            html.Div(
                                'Real / Plan acum.',
                                style={
                                    'fontSize': 'clamp(4.5px, 0.52vw, 5.2px)',
                                    'color': '#666666',
                                    'whiteSpace': 'nowrap',
                                    'lineHeight': '1.1',
                                    'marginTop': '0.5px',
                                    'overflow': 'hidden',
                                    'textOverflow': 'ellipsis',
                                    'maxWidth': '100%',
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
                                'CIERRE',
                                style={
                                    'fontWeight': '700',
                                    'fontSize': 'clamp(5.5px, 0.65vw, 6.5px)',
                                    'color': '#4a4a4a',
                                    'letterSpacing': '0.2px',
                                    'lineHeight': '1.1',
                                    'whiteSpace': 'nowrap',
                                },
                            ),
                            html.Div(
                                'Proy. / Plan día',
                                style={
                                    'fontSize': 'clamp(4.5px, 0.52vw, 5.2px)',
                                    'color': '#666666',
                                    'whiteSpace': 'nowrap',
                                    'lineHeight': '1.1',
                                    'marginTop': '0.5px',
                                    'overflow': 'hidden',
                                    'textOverflow': 'ellipsis',
                                    'maxWidth': '100%',
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
                                'RITMO',
                                style={
                                    'fontWeight': '700',
                                    'fontSize': 'clamp(5.5px, 0.65vw, 6.5px)',
                                    'color': '#4a4a4a',
                                    'letterSpacing': '0.2px',
                                    'lineHeight': '1.1',
                                    'whiteSpace': 'nowrap',
                                },
                            ),
                            html.Div(
                                'Req./h',
                                style={
                                    'fontSize': 'clamp(4.5px, 0.52vw, 5.2px)',
                                    'color': '#666666',
                                    'whiteSpace': 'nowrap',
                                    'lineHeight': '1.1',
                                    'marginTop': '0.5px',
                                    'overflow': 'hidden',
                                    'textOverflow': 'ellipsis',
                                    'maxWidth': '100%',
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


def build_row(
    *,
    label: str,
    index: int,
    real: str | int | float = '-',
    plan: str | int | float = '-',
    proyeccion: str | int | float = '-',
    objetivo_dia: str | int | float = '-',
    requerido: str | int | float = '-',
    **kwargs: Any,
):
    if isinstance(proyeccion, str):
        display_proyeccion = proyeccion.replace('*', '').strip()
    else:
        display_proyeccion = proyeccion

    # Cálculo directo de colores
    color_avance = _resolve_metric_color(real, plan)
    color_cierre = _resolve_metric_color(display_proyeccion, objetivo_dia)

    return html.Div(
        style={
            'borderBottom': '1px solid #d4d4d4',
            'paddingTop': '1.5px',
            'paddingBottom': '1.5px',
            'width': '100%',
            'boxSizing': 'border-box',
        },
        children=[
            # Etiqueta de la fila
            html.Div(
                f'{label} (kt)',
                style={
                    'fontSize': 'clamp(5.0px, 0.58vw, 5.8px)',
                    'color': '#555555',
                    'fontWeight': '500',
                    'lineHeight': '1.1',
                    'marginBottom': '0.5px',
                    'paddingLeft': '1px',
                    'whiteSpace': 'nowrap',
                },
            ),
            # Cuadrícula de métricas con color directo aplicado
            html.Div(
                style={
                    'display': 'grid',
                    'gridTemplateColumns': 'repeat(3, minmax(0, 1fr))',
                    'width': '100%',
                    'alignItems': 'baseline',
                    'lineHeight': '1.1',
                },
                children=[
                    # AVANCE: Real (Color directo) / Plan
                    html.Div(
                        style={
                            'minWidth': '0',
                            'display': 'flex',
                            'justifyContent': 'center',
                            'alignItems': 'baseline',
                            'gap': '1.5px',
                            'whiteSpace': 'nowrap',
                        },
                        children=[
                            html.Span(
                                f'{real}',
                                style={
                                    'fontWeight': '700',
                                    'fontSize': 'clamp(5.6px, 0.64vw, 6.6px)',
                                    'color': color_avance,
                                    'lineHeight': '1.1',
                                },
                            ),
                            html.Span(
                                f'/ {plan}',
                                style={
                                    'fontWeight': '400',
                                    'fontSize': 'clamp(4.8px, 0.55vw, 5.6px)',
                                    'color': '#666666',
                                    'lineHeight': '1.1',
                                },
                            ),
                        ],
                    ),
                    # CIERRE: Proy. (Color directo) / Plan día
                    html.Div(
                        style={
                            'minWidth': '0',
                            'display': 'flex',
                            'justifyContent': 'center',
                            'alignItems': 'baseline',
                            'gap': '1.5px',
                            'whiteSpace': 'nowrap',
                        },
                        children=[
                            html.Span(
                                f'{display_proyeccion}',
                                style={
                                    'fontWeight': '700',
                                    'fontSize': 'clamp(5.6px, 0.64vw, 6.6px)',
                                    'color': color_cierre,
                                    'lineHeight': '1.1',
                                },
                            ),
                            html.Span(
                                f'/ {objetivo_dia}',
                                style={
                                    'fontWeight': '400',
                                    'fontSize': 'clamp(4.8px, 0.55vw, 5.6px)',
                                    'color': '#666666',
                                    'lineHeight': '1.1',
                                },
                            ),
                        ],
                    ),
                    # RITMO: Req. /h
                    html.Div(
                        style={
                            'minWidth': '0',
                            'display': 'flex',
                            'justifyContent': 'center',
                            'alignItems': 'baseline',
                            'gap': '1.5px',
                            'whiteSpace': 'nowrap',
                        },
                        children=[
                            html.Span(
                                f'{requerido}',
                                style={
                                    'fontWeight': '700',
                                    'fontSize': 'clamp(5.6px, 0.64vw, 6.6px)',
                                    'color': '#4a4a4a',
                                    'lineHeight': '1.1',
                                },
                            ),
                            html.Span(
                                '/h',
                                style={
                                    'fontWeight': '400',
                                    'fontSize': 'clamp(4.8px, 0.55vw, 5.6px)',
                                    'color': '#666666',
                                    'lineHeight': '1.1',
                                },
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )