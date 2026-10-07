from __future__ import annotations

from typing import TYPE_CHECKING

from dash import html
from dash.development.base_component import Component

from src.shared.ui.charts.feeders import FeedersData
from src.shared.ui.charts.stockpile_mina import StockpileMinaData
from src.shared.ui.components.compact_table import CompactTableData

from ..chancador.models import ChancadorGroupData
from ..correa_stmg.models import CorreaStmgGroupData

if TYPE_CHECKING:
    from .models import ChancadoStmgData, ProduccionGlobalData, ProduccionGlobalMetricRow

_ROW_CLASS_NAME = 'd-flex flex-column gap-1 pb-1'


def build_chancado_stmg_component(*, model: ChancadoStmgData):
    return html.Div(
        className='d-flex flex-column gap-1 equipos-ch-wrapper',
        children=[
            _global_production_content(global_production_summary=model.produccion_global_summary),
            _equipos_ch_content(
                chancadores=model.chancadores,
                chancadores_summary=model.chancadores_summary,
                stockpile_mina=model.stockpile_mina,
                feeders=model.feeders,
            ),
            _correas_stmg_content(correas_stmg=model.correas_stmg),
            _leyes_content(leyes_summary=model.leyes_summary),
        ],
    )


def _global_production_content(*, global_production_summary: ProduccionGlobalData):
    return html.Div(
        className=_ROW_CLASS_NAME,
        children=[
            _title(label='Producción Global'),
            _build_produccion_global_table(summary=global_production_summary),
        ],
    )


def _build_produccion_global_table(*, summary: ProduccionGlobalData) -> Component:
    rows = [
        _build_produccion_global_row(row=item, index=index)
        for index, item in enumerate(summary.rows)
    ]

    return html.Div(
        className='w-100',
        style={'padding': '0 4px', 'boxSizing': 'border-box'},
        children=[
            # Encabezado (AVANCE / CIERRE / RITMO) simétrico de 3 columnas
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
                                'AVANCE',
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
                                'Real / Plan acum.',
                                style={
                                    'fontSize': 'clamp(5.8px, 0.75vw, 7px)',
                                    'color': '#555555',
                                    'whiteSpace': 'nowrap',
                                    'lineHeight': '1.2',
                                    'marginTop': '1px',
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
                                    'fontSize': 'clamp(7px, 0.9vw, 8px)',
                                    'color': '#515151',
                                    'letterSpacing': '0.3px',
                                    'lineHeight': '1.2',
                                    'whiteSpace': 'nowrap',
                                },
                            ),
                            html.Div(
                                'Proy. / Plan día',
                                style={
                                    'fontSize': 'clamp(5.8px, 0.75vw, 7px)',
                                    'color': '#555555',
                                    'whiteSpace': 'nowrap',
                                    'lineHeight': '1.2',
                                    'marginTop': '1px',
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
                                    'fontSize': 'clamp(7px, 0.9vw, 8px)',
                                    'color': '#515151',
                                    'letterSpacing': '0.3px',
                                    'lineHeight': '1.2',
                                    'whiteSpace': 'nowrap',
                                },
                            ),
                            html.Div(
                                'Req./h',
                                style={
                                    'fontSize': 'clamp(5.8px, 0.75vw, 7px)',
                                    'color': '#555555',
                                    'whiteSpace': 'nowrap',
                                    'lineHeight': '1.2',
                                    'marginTop': '1px',
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


def _build_produccion_global_row(*, row: ProduccionGlobalMetricRow, index: int) -> Component:
    proyeccion = str(row.proyeccion).replace('*', '').strip()

    return html.Div(
        style={
            'borderBottom': '1px solid #d0d0d0',
            'paddingTop': '3.5px',
            'paddingBottom': '3.5px',
            'width': '100%',
        },
        children=[
            # Etiqueta de la fila
            html.Div(
                f'{row.label} (kt)',
                style={
                    'fontSize': 'clamp(6.5px, 0.8vw, 7.5px)',
                    'color': '#4a4a4a',
                    'lineHeight': '1.2',
                    'marginBottom': '2px',
                    'paddingLeft': '2px',
                    'whiteSpace': 'nowrap',
                },
            ),
            # Cuadrícula con valores
            html.Div(
                style={
                    'display': 'grid',
                    'gridTemplateColumns': 'repeat(3, minmax(0, 1fr))',
                    'width': '100%',
                    'alignItems': 'baseline',
                },
                children=[
                    # AVANCE: Real / Plan
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
                                f'{row.real}',
                                style={
                                    'fontWeight': '700',
                                    'fontSize': 'clamp(7.5px, 0.95vw, 8.5px)',
                                    'color': '#515151',
                                    'lineHeight': '1.2',
                                },
                            ),
                            html.Span(
                                f'/ {row.plan}',
                                style={
                                    'fontSize': 'clamp(6.5px, 0.8vw, 7.5px)',
                                    'color': '#595959',
                                    'lineHeight': '1.2',
                                },
                            ),
                        ],
                    ),
                    # CIERRE: Proy. / Plan día
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
                                f'{proyeccion}',
                                style={
                                    'fontWeight': '700',
                                    'fontSize': 'clamp(7.5px, 0.95vw, 8.5px)',
                                    'color': '#515151',
                                    'lineHeight': '1.2',
                                },
                            ),
                            html.Span(
                                f'/ {row.objetivo_dia}',
                                style={
                                    'fontSize': 'clamp(6.5px, 0.8vw, 7.5px)',
                                    'color': '#595959',
                                    'lineHeight': '1.2',
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
                            'gap': '2px',
                            'whiteSpace': 'nowrap',
                        },
                        children=[
                            html.Span(
                                f'{row.requerido}',
                                style={
                                    'fontWeight': '700',
                                    'fontSize': 'clamp(7.5px, 0.95vw, 8.5px)',
                                    'color': '#515151',
                                    'lineHeight': '1.2',
                                },
                            ),
                            html.Span(
                                '/h',
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


def _equipos_ch_content(
    *,
    chancadores: ChancadorGroupData,
    chancadores_summary: CompactTableData,
    stockpile_mina: StockpileMinaData,
    feeders: FeedersData,
) -> Component:
    return html.Div(
        className=_ROW_CLASS_NAME,
        children=[
            _title(label='Equipos CH'),
            chancadores.to_component(),
            chancadores_summary.to_component(),
            html.Div(
                className='d-flex flex-column align-items-center justify-content-center w-100',
                children=[
                    html.Div(
                        className='stockpile-mina-wrapper w-100 d-flex justify-content-center',
                        children=[
                            stockpile_mina.to_component(),
                        ],
                    ),
                    html.P(className='font-size-100 fw-bold', children=['Stockpile Mina']),
                ],
            ),
            html.Div(
                className='d-flex flex-column align-items-center justify-content-center w-100',
                children=[
                    feeders.to_component(),
                    html.P(className='font-size-100 fw-bold', children=['FEEDERS']),
                ],
            ),
        ],
    )


def _correas_stmg_content(*, correas_stmg: CorreaStmgGroupData) -> Component:
    return html.Div(
        className=_ROW_CLASS_NAME,
        children=[
            _title(label='Correas STMG'),
            correas_stmg.to_group_component(),
        ],
    )


def _leyes_content(*, leyes_summary: CompactTableData):
    return html.Div(
        className=_ROW_CLASS_NAME, children=[_title(label='Leyes'), leyes_summary.to_component()]
    )


def _title(label: str):
    return html.Div(
        className='display-section-title fs-io-100',
        children=[html.P(children=[label.upper()])],
    )