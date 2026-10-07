from __future__ import annotations

from typing import TYPE_CHECKING

from dash import html
from dash.development.base_component import Component

from src.shared.ui.theme import resolve_color_class

if TYPE_CHECKING:
    from .models import ChancadoData


def build_chancado_stmg_component(*, model: ChancadoData) -> Component:
    wrapper_class_name = 'flex-row-reverse' if model.mirror else ''

    return html.Div(
        className=f'd-flex gap-1 {wrapper_class_name}',
        children=[
            html.Div(
                className='d-flex align-items-center',
                children=[_safe_image(value=model.chancado_state)],
            ),
            html.Div(className='d-flex align-items-center', children=[_content(model=model)]),
        ],
    )


def build_chancado_stmg_group_component(*, models: tuple[ChancadoData, ...]) -> Component:
    return html.Div(
        className='d-flex justify-content-evenly px-1',
        children=[chancador.to_component() for chancador in models],
    )


def _content(*, model: ChancadoData) -> Component:
    return html.Div(
        className='d-flex flex-column justify-content-start align-items-center',
        children=[
            html.P(className='fw-bold fs-io-200', children=[model.label.upper()]),
            html.Div(
                className='d-flex fs-io-300',
                children=[
                    html.P(
                        className=f'fw-bold{resolve_color_class(value=model.chancado_color)}',
                        children=[_safe_text(value=model.chancado_value)],
                    ),
                    _safe_unit(value=model.chancado_unit),
                ],
            ),
            _atollo_in_progress(atollo=model.atollo_state),
        ],
    )


def _atollo_in_progress(
    *,
    atollo: str | Component | None,
) -> Component | None:
    _class_name_text = 'fs-io-300'
    if atollo is None:
        return html.Div(className=f'text-transparent {_class_name_text}', children=['Sin Atollo'])

    if not isinstance(atollo, str):
        return atollo

    return (
        html.P(className=f'fst-italic text-red {_class_name_text}', children=['● Atollo'])
        if atollo == '1'
        else html.Div(className=f'text-transparent {_class_name_text}', children=['Sin Atollo'])
    )


def _safe_unit(value: str | None) -> Component | None:
    return (
        html.P(style={'paddingLeft': '.1rem'}, children=[_safe_text(value=value)])
        if value is not None
        else None
    )


def _safe_text(value: str | None | Component) -> Component | str:
    if value is None:
        return ''
    return value


def _safe_image(value: str | None | Component) -> Component:
    if value is None:
        return html.Img(src='/assets/img/icons/empty_data.svg')

    if not isinstance(value, str):
        return value

    return html.Img(
        className='img-fluid chancador-img',
        src='assets/img/industrial/chancador/{0}.svg'.format(value),
    )
