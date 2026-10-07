from __future__ import annotations

from typing import TYPE_CHECKING

from dash import html
from dash.development.base_component import Component

from src.shared.ui.theme import resolve_color_class

if TYPE_CHECKING:
    from .models import (
        CompactCardData,
        CompactCardGroupData,
        CompactCardRowData,
        CompactCardValueData,
    )

_ALLOWED_INDICATOR_POSITIONS = {'top', 'left'}


def build_compact_card_component(
    *,
    model: CompactCardData,
) -> Component:
    return html.Div(
        className=_join_class_names(
            'compact-card-wrapper',
            model.wrapper_class_name,
        ),
        children=[
            html.Div(
                className=(
                    'compact-card d-flex flex-column '
                    'justify-content-center align-items-center '
                    # f'{resolve_color_class(value=model.card_color, color_type="background", variant_type="soft")}'
                ),
                children=[
                    html.Div(
                        className=(
                            'compact-card-header d-flex justify-content-between '
                            'align-items-center w-100 gap-1'
                        ),
                        children=[
                            _safe_title(
                                title=model.title.label,
                                class_name=model.title.label_class_name,
                            ),
                            _safe_title(
                                title=model.title.extra_label,
                                class_name=model.title.extra_label_class_name,
                                is_extra_title=True,
                            ),
                        ],
                    ),
                    _build_columns(values=model.values),
                ],
            )
        ],
    )


def build_compact_card_group_component(
    *,
    model: CompactCardGroupData,
) -> Component:
    indicator_position = _normalize_indicator_position(value=model.indicator_position)

    wrapper_content = ''
    wrapper_content_shell = ''
    if model.wrapper_class_name is not None:
        wrapper_content = 'content-extra-position'
        wrapper_content_shell = 'wrapper-content-shell'

    return html.Div(
        className=_join_class_names(
            'compact-card-group',
            f'compact-card-group-indicator-{indicator_position} '
            f'{model.wrapper_class_name or ""}'.strip(),
        ),
        children=[
            _build_indicator(
                indicator=model.indicator, use_marker=model.wrapper_class_name is not None
            ),
            html.Div(
                className=f'compact-card-group-content-shell {wrapper_content_shell}',
                children=[
                    html.Div(
                        className=f'compact-card-group-content {wrapper_content}',
                        children=[build_compact_card_component(model=card) for card in model.cards],
                    )
                ],
            ),
        ],
    )


def build_compact_card_row_component(
    *,
    model: CompactCardRowData,
) -> Component:
    return html.Div(
        className='compact-card-row d-flex flex-column gap-2',
        children=[build_compact_card_group_component(model=row) for row in model.rows],
    )


def _build_indicator(*, indicator: str | None, use_marker: bool = False) -> Component | None:
    if indicator is None:
        return None

    return html.Div(
        className=f'compact-card-row-indicator-wrapper {"indicator-marker" if use_marker else ""}'.strip(),
        children=[
            html.P(
                className='compact-card-row-indicator',
                children=[indicator],
            )
        ],
    )


def _safe_title(
    *,
    title: str | None,
    class_name: str,
    is_extra_title: bool = False,
) -> Component | None:
    if title is None:
        return None

    title_type_class_name = 'extra-title' if is_extra_title else 'title'

    return html.P(
        className=_join_class_names(
            'compact-card-title',
            title_type_class_name,
            class_name,
        ),
        children=[title],
    )


def _build_columns(
    *,
    values: tuple[CompactCardValueData, ...],
) -> Component:
    return html.Div(
        className='compact-card-values',
        children=[_build_column(value=value) for value in values],
    )


def _build_column(
    *,
    value: CompactCardValueData,
) -> Component:
    return html.Div(
        className='compact-card-column',
        children=[
            html.P(
                className=_join_class_names(
                    'compact-card-label',
                    value.label_class_name,
                    'lh-1',
                ),
                children=[value.label],
            ),
            html.P(
                className=_join_class_names(
                    'compact-card-value',
                    value.value_class_name,
                    # resolve_color_class(value=value.color, variant_type='strong'),
                ),
                children=[_safe_value(value=value.value)],
            ),
        ],
    )


def _safe_value(value: str | None | Component) -> str | None:
    if value is None:
        return html.Img(
            src='assets/img/icons/empty_data.svg', className='empty-data-icon img-fluid'
        )
    return value


def _normalize_indicator_position(*, value: str | None) -> str:
    if value in _ALLOWED_INDICATOR_POSITIONS:
        return value
    return 'top'


def _join_class_names(*values: str | None) -> str:
    return ' '.join(value for value in values if value)
