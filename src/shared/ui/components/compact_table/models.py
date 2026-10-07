from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, Literal, Mapping, TypeAlias

from dash.development.base_component import Component

from .build import (
    build_compact_table_component,
    build_compact_table_replacement_component,
)

DisplayValue: TypeAlias = str | int | float | Component | None
CellAlign: TypeAlias = Literal['start', 'center', 'end']


@dataclass(frozen=True, slots=True)
class CompactTableColumnData:
    key: str
    label: DisplayValue = ''
    align: CellAlign = 'end'
    header_align: CellAlign | None = None
    width: str | None = None
    class_name: str = ''
    header_class_name: str = ''
    is_row_header: bool = False


@dataclass(frozen=True, slots=True)
class CompactTableCellData:
    value: DisplayValue = None
    color: DisplayValue = None
    align: CellAlign | None = None
    class_name: str = ''
    emphasized: bool = False
    title: str | None = None

    @classmethod
    def of(
        cls,
        value: DisplayValue,
        *,
        color: DisplayValue = None,
        align: CellAlign | None = None,
        class_name: str = '',
        emphasized: bool = False,
        title: str | None = None,
    ) -> CompactTableCellData:
        return cls(
            value=value,
            color=color,
            align=align,
            class_name=class_name,
            emphasized=emphasized,
            title=title,
        )


CellInput: TypeAlias = DisplayValue | CompactTableCellData


@dataclass(frozen=True, slots=True)
class CompactTableRowData:
    key: str
    cells: Mapping[str, CellInput] = field(default_factory=dict)

    span_value: DisplayValue = None
    is_span: bool = False

    color: DisplayValue = None
    class_name: str = ''
    emphasized: bool = False
    first_cell_marker: bool = False

    @classmethod
    def data(
        cls,
        *,
        key: str,
        cells: Mapping[str, CellInput],
        color: DisplayValue = None,
        class_name: str = '',
        emphasized: bool = False,
        first_cell_marker: bool = False,
    ) -> CompactTableRowData:
        return cls(
            key=key,
            cells=cells,
            color=color,
            class_name=class_name,
            emphasized=emphasized,
            first_cell_marker=first_cell_marker,
        )

    @classmethod
    def span(
        cls,
        *,
        key: str,
        value: DisplayValue,
        color: DisplayValue = None,
        class_name: str = '',
        emphasized: bool = True,
    ) -> CompactTableRowData:
        return cls(
            key=key,
            span_value=value,
            is_span=True,
            color=color,
            class_name=class_name,
            emphasized=emphasized,
        )


@dataclass(frozen=True, slots=True)
class CompactTableData:
    columns: tuple[CompactTableColumnData, ...]
    rows: tuple[CompactTableRowData, ...]

    has_replacement: bool = False
    replacement_value: DisplayValue = None

    show_header: bool = True
    class_name: str = ''
    wrapper_class_name: str = ''

    emphasized: bool = True

    @classmethod
    def replacement(
        cls,
        *,
        value: DisplayValue = None,
        columns: Iterable[CompactTableColumnData] = (),
        class_name: str = '',
        wrapper_class_name: str = '',
    ) -> CompactTableData:
        return cls(
            columns=tuple(columns),
            rows=(),
            has_replacement=True,
            replacement_value=value,
            class_name=class_name,
            wrapper_class_name=wrapper_class_name,
        )

    @classmethod
    def from_iterable(
        cls,
        *,
        columns: Iterable[CompactTableColumnData],
        rows: Iterable[CompactTableRowData],
        show_header: bool = True,
        class_name: str = '',
        wrapper_class_name: str = '',
        emphasized: bool = True,
    ) -> CompactTableData:
        return cls(
            columns=tuple(columns),
            rows=tuple(rows),
            show_header=show_header,
            class_name=class_name,
            wrapper_class_name=wrapper_class_name,
            emphasized=emphasized,
        )

    def to_component(self) -> Component:
        if self.has_replacement:
            return build_compact_table_replacement_component(
                value=self.replacement_value,
            )

        return build_compact_table_component(
            columns=self.columns,
            rows=self.rows,
            show_header=self.show_header,
            class_name=self.class_name,
            wrapper_class_name=self.wrapper_class_name,
            emphasized=self.emphasized,
        )

    def to_components(self) -> list[Component]:
        return [self.to_component()]

    def __iter__(self):
        return iter(self.rows)

    def __len__(self) -> int:
        return len(self.rows)
