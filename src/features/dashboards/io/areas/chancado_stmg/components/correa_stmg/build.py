from __future__ import annotations

from typing import TYPE_CHECKING

from dash import html
from dash.development.base_component import Component

if TYPE_CHECKING:
    from .models import CorreaStmgData, CorreaStmgGroupData


def build_correa_stmg_component(*, model: CorreaStmgData, position: int = 1) -> Component:
    return html.Div(
        className='d-flex flex-column justify-content-center align-items-center gap-1',
        children=[
            _safe_image(value=model.correa_state, position=position),
            html.P(className='fw-bold fs-io-200', children=[model.label.upper()]),
        ],
    )


def build_correas_stmg_component(*, models: tuple[CorreaStmgData, ...]) -> Component:
    return html.Div(
        className='d-flex justify-content-between w-100',
        children=[
            model.to_component(position=index) for index, model in enumerate(models, start=1)
        ],
    )


def build_correa_stmg_group_component(
    *,
    models: CorreaStmgGroupData,
) -> Component:
    return html.Div(
        className='d-flex flex-column justify-content-center align-items-center gap-1',
        children=[
            models.to_component(),
            html.Div(className='d-flex w-100', children=models.metrics.to_components()),
        ],
    )


def _safe_image(value: str | None | Component, position: int) -> Component:
    if value is None:
        return html.Img(
            className='correa-smg-img-position-{0}'.format(position),
            src='assets/img/icons/empty_data.svg',
        )

    if not isinstance(value, str):
        return value

    return html.Img(
        className='img-fluid correa-stmg-img correa-smg-img-position-{0}'.format(position),
        src='assets/img/industrial/correa_stmg/{0}.svg'.format(value),
    )
