from __future__ import annotations

from dash import html


def build_managed_alarms_modal_footer() -> html.Div:
    return html.Div(
        className='managed-alarms-modal-footer',
        children=[
            html.Div(
                className='managed-alarms-legend',
                children=[
                    html.Span('Leyenda de severidad:'),
                    _build_legend_item('impacto', 'Impacto'),
                    _build_legend_item('riesgo', 'Riesgo'),
                    # _build_legend_item('inactive', 'Desactivada'),
                ],
            ),
            html.Div(
                className='managed-alarms-footer-note',
                children=[
                    html.I(className='bi bi-info-circle'),
                    html.Span('Vista congelada: los datos se recargan al presionar Actualizar.'),
                ],
            ),
        ],
    )


def _build_legend_item(
    severity_code: str,
    label: str,
) -> html.Div:
    return html.Div(
        className='managed-alarms-legend-item',
        children=[
            html.Span(
                className=(f'managed-alarms-legend-dot managed-alarms-legend-dot-{severity_code}'),
            ),
            html.Span(children=[label]),
        ],
    )
