from __future__ import annotations

from typing import Any

from dash import html
from dash.development.base_component import Component

from src.shared.ui.theme import resolve_color_class

ALIGN_CLASS_NAMES = {
    'start': 'text-start',
    'center': 'text-center',
    'end': 'text-end',
}


def build_colgroup(
    *,
    columns: tuple[Any, ...],
) -> Component | None:
    if not columns or not any(column.width for column in columns):
        return None

    return html.Colgroup(
        children=[
            html.Col(
                style={'width': column.width} if column.width else {},
            )
            for column in columns
        ],
    )


def build_table_header(
    *,
    columns: tuple[Any, ...],
    emphasized: bool = True,
) -> Component:
    emphasized_class_name = 'emphasized' if emphasized else 'transparent'

    return html.Thead(
        children=[
            html.Tr(
                className=f'compact-table-header-row {emphasized_class_name}',
                children=[
                    _build_header_cell(
                        column=column,
                        is_end=index == len(columns),
                    )
                    for index, column in enumerate(columns, start=1)
                ],
            ),
        ],
    )


def build_table_body(
    *,
    columns: tuple[Any, ...],
    rows: tuple[Any, ...],
) -> Component:
    return html.Tbody(
        children=[
            _build_row(
                columns=columns,
                row=row,
            )
            for row in rows
        ],
    )


def _build_header_cell(
    *,
    column: Any,
    is_end: bool,
) -> Component:
    align = column.header_align or column.align
    cell_end_label = 'cell-header-end' if is_end else ''

    return html.Th(
        className=_join_class_names(
            'compact-table-header-cell',
            ALIGN_CLASS_NAMES.get(align, ''),
            column.header_class_name,
        ),
        children=[
            html.P(
                className=_join_class_names(
                    'compact-table-cell-text',
                    cell_end_label,
                ),
                children=[column.label],
            ),
        ],
    )


def _build_row(
    *,
    columns: tuple[Any, ...],
    row: Any,
) -> Component:
    if row.is_span:
        return _build_span_row(
            columns=columns,
            row=row,
        )

    return _build_data_row(
        columns=columns,
        row=row,
    )


def _build_span_row(
    *,
    columns: tuple[Any, ...],
    row: Any,
) -> Component:
    color_class_name = _resolve_text_color_class(row.color)
    emphasized_class_name = 'emphasized' if row.emphasized else 'transparent'

    return html.Tr(
        key=row.key,
        className=_join_class_names(
            'compact-table-body-row',
            'compact-table-body-row--span',
            row.class_name,
        ),
        children=[
            html.Td(
                colSpan=len(columns),
                className=_join_class_names(
                    'compact-table-body-span-row',
                    emphasized_class_name,
                    color_class_name,
                ),
                children=[
                    html.Div(
                        className='compact-table-cell-content',
                        children=[
                            html.P(
                                className='compact-table-cell-text',
                                children=[row.span_value],
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )


def _build_data_row(
    *,
    columns: tuple[Any, ...],
    row: Any,
) -> Component:
    return html.Tr(
        key=row.key,
        className=_join_class_names(
            'compact-table-body-row',
            row.class_name,
        ),
        children=[
            _build_data_cell(
                column=column,
                row=row,
                is_first=index == 1,
                is_end=index == len(columns),
            )
            for index, column in enumerate(columns, start=1)
        ],
    )


def _build_data_cell(
    *,
    column: Any,
    row: Any,
    is_first: bool,
    is_end: bool,
) -> Component:
    cell = _normalize_cell(
        value=row.cells.get(column.key),
    )

    align = cell.align or column.align
    color = cell.color if cell.color is not None else row.color

    color_class_name = _resolve_text_color_class(color)
    emphasized_class_name = 'fw-semibold' if cell.emphasized or row.emphasized else ''
    align_class_name = ALIGN_CLASS_NAMES.get(align, '')

    cell_tag = html.Th if column.is_row_header else html.Td
    cell_kwargs = {'scope': 'row'} if column.is_row_header else {}
    cell_label_class_name = 'cell-body-label-row' if column.is_row_header else ''
    cell_end_class_name = 'cell-body-end' if is_end else ''

    return cell_tag(
        className=_join_class_names(
            'compact-table-body-cell',
            align_class_name,
            color_class_name,
            emphasized_class_name,
            column.class_name,
            cell.class_name,
        ),
        title=cell.title,
        children=[
            html.Div(
                className=_join_class_names(
                    'compact-table-cell-content',
                    cell_label_class_name,
                    cell_end_class_name,
                ),
                children=_build_cell_children(
                    cell=cell,
                    is_first_cell=is_first,
                    show_marker=is_first and row.first_cell_marker,
                ),
            ),
        ],
        **cell_kwargs,
    )


def _build_cell_children(
    *,
    cell: Any,
    is_first_cell: bool = False,
    show_marker: bool = False,
) -> list[Component]:
    children: list[Component] = []

    if show_marker:
        children.append(
            html.P(
                className='compact-table-cell-marker',
            ),
        )

    children.append(
        html.P(
            className=f'compact-table-cell-text {"strong-value" if not is_first_cell else ""}',
            children=[_safe_text(value=cell.value)],
        ),
    )

    return children


def _normalize_cell(
    *,
    value: Any,
) -> Any:
    from .models import CompactTableCellData

    if isinstance(value, CompactTableCellData):
        return value

    return CompactTableCellData(
        value=value,
    )


def _resolve_text_color_class(
    value: Any,
) -> str:
    if value is None:
        return ''

    return resolve_color_class(
        value=value,
        color_type='text',
    )


def _safe_text(value: Any) -> Component | Any:
    if value is None:
        return html.Img(
            className='compact-table-empty-data-icon',
            src='assets/img/icons/not_mapped.svg',
            alt='Sin dato',
        )

    return value


def _join_class_names(*values: str | None) -> str:
    return ' '.join(value.strip() for value in values if value and value.strip())
