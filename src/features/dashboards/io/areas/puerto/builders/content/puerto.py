from __future__ import annotations

from dash import html
from dash.development.base_component import Component
from src.shared.ui.charts.level_gauge import LevelGaugeDefinition, map_level_gauge
from src.shared.ui.display import build_inline_value_row


def build_puerto_content(kpis: dict):
    value, unit, indicator = resolve_closed_duration(kpis.get('embarque_tiempo_actual_inst'))

    items = {}
    counter = 1
    temp_list = []
    for fl_number in ('001', '002', '003', '004', '005', '006', '702', '703'):
        if len(temp_list) == 4:
            counter += 1
            temp_list.clear()

        temp_list.append(state_component(label=f'FL-{fl_number}', state=kpis.get(f'fl_{fl_number}_estado_inst')))
        if counter not in items:
            items[counter] = temp_list.copy()
            continue
        items[counter] = temp_list.copy()


    return html.Div(
        className='d-flex flex-column gap-1',
        children=[
            html.Div(
                className='d-flex flex-column gap-1',
                children=[
                    _title('--'),
                    html.Div(
                        className='d-flex justify-content-evenly w-100',
                        children=[
                            _level_gauge(tk_number='60', state='operando', kpis=kpis),
                            _level_gauge(tk_number='61', state='operando', kpis=kpis),
                            _level_gauge(tk_number='62', state='operando', kpis=kpis),
                            _level_gauge(tk_number='63', state='operando', kpis=kpis),
                        ]
                    ),
                ]
            ),
            html.Div(
                className='d-flex flex-column gap-1',
                children=[
                    _title('Filtros'),
                    html.Div(
                        className='d-flex flex-column gap-1',
                        children=[
                            html.Div(
                                className='d-flex justify-content-between align-items-center gap-1',
                                children=[
                                    *items.get(1)
                                ]
                            ),
                            html.Div(
                                className='d-flex justify-content-between align-items-center gap-1',
                                children=[
                                    *items.get(2)
                                ]
                            )
                        ]
                    )
                ]
            ),
            html.Div(
                className='d-flex flex-column gap-1',
                children=[
                    _title('Embarque'),
                    html.Div(
                        className='d-flex w-100 gap-2 align-items-center',
                        children=[
                            html.Div(
                                className='d-flex flex-column w-100',
                                children=[
                                    build_inline_value_row(
                                        label='Tonelaje',
                                        value=kpis.get('embarque_tonelaje_actual_inst'),
                                        unit='TMH',
                                        color='',
                                        container_class_name='app-border-bottom pt-1',
                                        font_size_class_name='fs-io-bc-200'
                                    ),
                                    build_inline_value_row(
                                        label='Tiempo',
                                        value=f'{indicator}{value}',
                                        unit=unit,
                                        color='',
                                        container_class_name='app-border-bottom pt-1',
                                        font_size_class_name='fs-io-bc-200'
                                    )
                                ]
                            ),
                            html.Div(
                                className='d-flex justify-content-center align-items-center',
                                children=[
                                    html.Img(
                                        className='img-fluid barco-img',
                                        src='assets/img/industrial/barco/{0}.svg'.format(kpis.get('embarque_estado_inst'))
                                    )
                                ]
                            ),
                        ]
                    )
                ]
            )
        ]
    )



def _level_gauge(tk_number: str, state: str, kpis: dict):
    definition = LevelGaugeDefinition(
        number=tk_number,
        variant='tk',
        image_name='tk',
        name_prefix='TK',
        tag_prefix='tk',
    )

    data = map_level_gauge(
        definition=definition,
        kpis=kpis,
        override_state=state
    )

    return data.to_component()


def _title(title: str) -> Component:
    return html.Div(
        className='display-section-title fs-io-bc-100',
        children=[html.P(children=[title])],
    )

# def state_component(label: str, state: str):
#     normalized_state = state.strip().lower()
#
#     return html.Span(
#         className='flotation-state',
#         children=[
#             html.P(
#                 className='flotation-state__label fs-io-bc-100 fw-bold',
#                 children=label,
#             ),
#             html.Div(
#                 className='w-100 d-flex justify-content-center',
#                 children=[
#                     html.Img(
#                         className='flotation-state__icon',
#                         src='assets/img/industrial/circle_status/{0}.svg'.format(normalized_state),
#                         alt=normalized_state.capitalize(),
#                     ),
#                 ]
#             )
#         ],
#     )

def state_component(label: str, state: str):
    return html.Div(
        className='d-flex flex-column align-items-center',
        style={'border': '1px solid #bbbbbb', 'borderRadius': '5px', 'padding': '.2rem .1rem'},
        children=[
            html.P(
                className='fs-io-bc-100 fw-bold',
                children=[label]
            ),
            html.Img(
                className='img-fluid filtro-img',
                src='assets/img/industrial/filtro/{0}.svg'.format(state)
            )
        ]
    )

def resolve_closed_duration(total_seconds: int | float) -> tuple[int, str, str]:
    if total_seconds is None or isinstance(total_seconds, Component):
        return total_seconds, '', ''
    seconds = max(0, int(total_seconds))

    if seconds == 0:
        return 0, '', ''

    if seconds < 60:
        return seconds, "s", ''

    if seconds < 3_600:
        return seconds // 60, "m", ''

    if seconds < 86_400:
        return seconds // 3_600, "h", '>'

    return seconds // 86_400, "d", '>'

