from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, Literal, Mapping, TypeAlias

from dash.development.base_component import Component

DisplayValue: TypeAlias = str | int | float | Component | None
CellAlign: TypeAlias = Literal['start', 'center', 'end']


@dataclass(frozen=True, slots=True)
class TableValueDefinition:
    value: DisplayValue = None
    key: str | None = None
    default: DisplayValue = None
    template: str | None = None

    @classmethod
    def static(
        cls,
        value: DisplayValue,
    ) -> TableValueDefinition:
        return cls(
            value=value,
        )

    @classmethod
    def from_key(
        cls,
        key: str,
        *,
        default: DisplayValue = None,
        template: str | None = None,
    ) -> TableValueDefinition:
        return cls(
            key=key,
            default=default,
            template=template,
        )


@dataclass(frozen=True, slots=True)
class CompactTableColumnDefinition:
    key: str
    label: DisplayValue = ''
    align: CellAlign = 'end'
    header_align: CellAlign | None = None
    width: str | None = None
    class_name: str = ''
    header_class_name: str = ''
    is_row_header: bool = False


@dataclass(frozen=True, slots=True)
class CompactTableCellDefinition:
    value: TableValueDefinition = field(default_factory=TableValueDefinition)
    color: TableValueDefinition = field(default_factory=TableValueDefinition)
    title: TableValueDefinition = field(default_factory=TableValueDefinition)

    align: CellAlign | None = None
    class_name: str = ''
    class_name_key: str | None = None
    emphasized: bool = False
    emphasized_key: str | None = None

    @classmethod
    def static(
        cls,
        value: DisplayValue,
        *,
        color: DisplayValue = None,
        align: CellAlign | None = None,
        class_name: str = '',
        emphasized: bool = False,
        title: DisplayValue = None,
    ) -> CompactTableCellDefinition:
        return cls(
            value=TableValueDefinition.static(value),
            color=TableValueDefinition.static(color),
            title=TableValueDefinition.static(title),
            align=align,
            class_name=class_name,
            emphasized=emphasized,
        )

    @classmethod
    def from_key(
        cls,
        key: str,
        *,
        default: DisplayValue = None,
        template: str | None = None,
        color: DisplayValue = None,
        color_key: str | None = None,
        title: DisplayValue = None,
        title_key: str | None = None,
        align: CellAlign | None = None,
        class_name: str = '',
        class_name_key: str | None = None,
        emphasized: bool = False,
        emphasized_key: str | None = None,
    ) -> CompactTableCellDefinition:
        return cls(
            value=TableValueDefinition.from_key(
                key=key,
                default=default,
                template=template,
            ),
            color=TableValueDefinition(
                value=color,
                key=color_key,
            ),
            title=TableValueDefinition(
                value=title,
                key=title_key,
            ),
            align=align,
            class_name=class_name,
            class_name_key=class_name_key,
            emphasized=emphasized,
            emphasized_key=emphasized_key,
        )


@dataclass(frozen=True, slots=True)
class CompactTableRowDefinition:
    key: str | None = None
    key_key: str | None = None

    cells: Mapping[str, CompactTableCellDefinition] = field(default_factory=dict)

    is_span: bool = False
    is_span_key: str | None = None
    span_value: TableValueDefinition = field(default_factory=TableValueDefinition)

    color: TableValueDefinition = field(default_factory=TableValueDefinition)
    class_name: str = ''
    class_name_key: str | None = None

    emphasized: bool = False
    emphasized_key: str | None = None

    first_cell_marker: bool = False
    first_cell_marker_key: str | None = None

    @classmethod
    def data(
        cls,
        *,
        key: str | None = None,
        key_key: str | None = None,
        cells: Mapping[str, CompactTableCellDefinition],
        color: DisplayValue = None,
        color_key: str | None = None,
        class_name: str = '',
        class_name_key: str | None = None,
        emphasized: bool = False,
        emphasized_key: str | None = None,
        first_cell_marker: bool = False,
        first_cell_marker_key: str | None = None,
        is_span_key: str | None = None,
        span_value: DisplayValue = None,
        span_value_key: str | None = None,
    ) -> CompactTableRowDefinition:
        return cls(
            key=key,
            key_key=key_key,
            cells=cells,
            is_span_key=is_span_key,
            span_value=TableValueDefinition(
                value=span_value,
                key=span_value_key,
            ),
            color=TableValueDefinition(
                value=color,
                key=color_key,
            ),
            class_name=class_name,
            class_name_key=class_name_key,
            emphasized=emphasized,
            emphasized_key=emphasized_key,
            first_cell_marker=first_cell_marker,
            first_cell_marker_key=first_cell_marker_key,
        )

    @classmethod
    def span(
        cls,
        *,
        key: str | None = None,
        key_key: str | None = None,
        value: DisplayValue = None,
        value_key: str | None = None,
        color: DisplayValue = None,
        color_key: str | None = None,
        class_name: str = '',
        class_name_key: str | None = None,
        emphasized: bool = True,
        emphasized_key: str | None = None,
    ) -> CompactTableRowDefinition:
        return cls(
            key=key,
            key_key=key_key,
            is_span=True,
            span_value=TableValueDefinition(
                value=value,
                key=value_key,
            ),
            color=TableValueDefinition(
                value=color,
                key=color_key,
            ),
            class_name=class_name,
            class_name_key=class_name_key,
            emphasized=emphasized,
            emphasized_key=emphasized_key,
        )


@dataclass(frozen=True, slots=True)
class CompactTableJsonRecordsSource:
    kpi_key: str

    row_key: str | None = None
    row_header_key: str | None = None
    row_header_label: DisplayValue | None = None

    section_key: str | None = None
    span_rows_when_only_row_header: bool = False

    records_key: str | None = None



@dataclass(frozen=True, slots=True)
class CompactTableDefinition:
    columns: tuple[CompactTableColumnDefinition, ...]
    rows: tuple[CompactTableRowDefinition, ...] = field(default_factory=tuple)

    json_records_source: CompactTableJsonRecordsSource | None = None

    show_header: bool = True
    class_name: str = ''
    wrapper_class_name: str = ''

    emphasized: bool = True

    @classmethod
    def from_iterable(
        cls,
        *,
        columns: Iterable[CompactTableColumnDefinition],
        rows: Iterable[CompactTableRowDefinition],
        show_header: bool = True,
        class_name: str = '',
        wrapper_class_name: str = '',
        emphasized: bool = True,
        json_records_source: CompactTableJsonRecordsSource | None = None,
    ) -> CompactTableDefinition:
        return cls(
            columns=tuple(columns),
            rows=tuple(rows),
            show_header=show_header,
            class_name=class_name,
            wrapper_class_name=wrapper_class_name,
            emphasized=emphasized,
            json_records_source=json_records_source,
        )
