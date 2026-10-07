from __future__ import annotations

from typing import Any, TypeAlias

from dash import html
from dash.development.base_component import Component

from .primitives import table, title


DisplayValue: TypeAlias = str | int | float | Component | None

DISPLAY_CARD_STATUS_BACKDROP_TYPE = 'display-card-status-backdrop'


def build_global_indicator_group_component(
    *,
    indicators: tuple[Any, ...],
) -> Component:
    return html.Div(
        className='global-indicator-container',
        children=[
            indicator.to_component()
            for indicator in indicators
        ],
    )


def build_global_indicator_component(
    *,
    uuid: str,
    indicator: DisplayValue,
    unit: DisplayValue,
    real_dia: DisplayValue,
    plan_dia: DisplayValue,
    real_semana: DisplayValue,
    plan_semana: DisplayValue,
    color_dia: DisplayValue = None,
    color_semana: DisplayValue = None,
    border_left: bool = False,
    border_right: bool = False,
) -> Component:
    border_left_class_name = (
        'border-left'
        if border_left
        else ''
    )
    border_right_class_name = (
        'border-right'
        if border_right
        else ''
    )

    return html.Div(
        className=(
            'global-indicator-wrapper position-relative '
            f'{border_left_class_name} '
            f'{border_right_class_name}'
        ),
        children=[
            title(
                indicator=indicator,
                unit=unit,
            ),
            table(
                real_dia=real_dia,
                plan_dia=plan_dia,
                color_dia=color_dia,
                real_semana=real_semana,
                plan_semana=plan_semana,
                color_semana=color_semana,
            ),
            build_status_backdrop(
                uuid=uuid,
            ),
            # last_measurement(
            #     real_turno=real_turno,
            # ),
        ],
    )


def build_status_backdrop(
    *,
    uuid: str,
    message: str = 'Datos desactualizados',
) -> Component:
    return html.Div(
        id={
            'type': DISPLAY_CARD_STATUS_BACKDROP_TYPE,
            'index': uuid,
        },
        className='display-card-backdrop',
        children=[
            html.Div(
                className='display-card-backdrop__content',
                children=[
                    html.I(
                        className=(
                            'bi bi-cloud-slash '
                            'display-card-backdrop__icon'
                        ),
                    ),
                    html.P(
                        className='display-card-backdrop__message',
                        children=[message],
                    ),
                ],
            ),
        ],
    )