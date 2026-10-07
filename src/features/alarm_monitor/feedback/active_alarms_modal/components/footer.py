from __future__ import annotations

from dash import html


def build_active_alarms_modal_footer() -> html.Div:
    return html.Div(
        className='active-alarms-modal-footer',
        children=[
            html.Div(
                className='active-alarms-legend',
                children=[
                    html.Span('Leyenda de severidad:'),
                    _build_legend_item('impacto', 'Impacto'),
                    _build_legend_item('riesgo', 'Riesgo'),
                    _build_legend_item('impacto-inactiva', 'Impacto - Inactiva'),
                    _build_legend_item('riesgo-inactiva', 'Riesgo - Inactiva'),
                ],
            ),
            html.Div(
                className='active-alarms-footer-note',
                children=[
                    html.I(className='bi bi-info-circle'),
                    html.Span(
                        'Vista congelada: los cambios nuevos se aplican al presionar Actualizar.'
                    ),
                ],
            ),
        ],
    )


def _build_legend_item(
    severity_code: str,
    label: str,
) -> html.Div:
    return html.Div(
        className='active-alarms-legend-item',
        children=[
            html.Span(
                className=f'active-alarms-legend-dot active-alarms-legend-dot-{severity_code}'
            ),
            html.Span(label),
        ],
    )
