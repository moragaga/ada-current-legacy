from __future__ import annotations

from typing import Any, Iterable, Mapping

from .definitions import (
    CompactTableCellDefinition,
    CompactTableColumnDefinition,
    CompactTableDefinition,
    CompactTableJsonRecordsSource,
    CompactTableRowDefinition,
    DisplayValue,
    TableValueDefinition,
)
from .models import (
    CompactTableCellData,
    CompactTableColumnData,
    CompactTableData,
    CompactTableRowData,
)

_MISSING = object()


def map_compact_table(
    *,
    definition: CompactTableDefinition,
    kpis: Mapping[str, Any],
) -> CompactTableData:
    if definition.json_records_source is not None:
        return _map_compact_table_from_json_source(
            definition=definition,
            source=definition.json_records_source,
            kpis=kpis,
        )

    return CompactTableData(
        columns=_map_columns(
            definitions=definition.columns,
        ),
        rows=tuple(
            map_compact_table_row(
                definition=row_definition,
                kpis=kpis,
                row_index=index,
            )
            for index, row_definition in enumerate(definition.rows)
        ),
        show_header=definition.show_header,
        class_name=definition.class_name,
        wrapper_class_name=definition.wrapper_class_name,
        emphasized=definition.emphasized,
    )


def _map_compact_table_from_json_source(
    *,
    definition: CompactTableDefinition,
    source: CompactTableJsonRecordsSource,
    kpis: Mapping[str, Any],
) -> CompactTableData:
    records_or_default = _resolve_json_source_records(
        source=source,
        kpis=kpis,
    )

    if isinstance(records_or_default, _JsonSourceDefault):
        return CompactTableData.replacement(
            value=records_or_default.value,
            columns=_map_columns(definitions=definition.columns),
            class_name=definition.class_name,
            wrapper_class_name=definition.wrapper_class_name,
        )

    records = tuple(records_or_default)
    if not records:
        return CompactTableData.replacement(
            value=None,
            columns=_map_columns(definitions=definition.columns),
            class_name=definition.class_name,
            wrapper_class_name=definition.wrapper_class_name,
        )

    column_keys = tuple(column.key for column in definition.columns) or None
    column_definitions = {column.key: column for column in definition.columns}

    return map_compact_table_json_records(
        records=records,
        column_keys=column_keys,
        column_definitions=column_definitions,
        row_key=source.row_key,
        row_header_key=source.row_header_key,
        row_header_label=source.row_header_label,
        section_key=source.section_key,
        span_rows_when_only_row_header=source.span_rows_when_only_row_header,
        show_header=definition.show_header,
        class_name=definition.class_name,
        wrapper_class_name=definition.wrapper_class_name,
        emphasized=definition.emphasized,
    )


def map_compact_table_records(
    *,
    columns: tuple[CompactTableColumnDefinition, ...],
    row_definition: CompactTableRowDefinition,
    records: Iterable[Mapping[str, Any]],
    show_header: bool = True,
    class_name: str = '',
    wrapper_class_name: str = '',
) -> CompactTableData:
    return CompactTableData(
        columns=_map_columns(
            definitions=columns,
        ),
        rows=tuple(
            map_compact_table_row(
                definition=row_definition,
                kpis=record,
                row_index=index,
            )
            for index, record in enumerate(records)
        ),
        show_header=show_header,
        class_name=class_name,
        wrapper_class_name=wrapper_class_name,
    )


def map_compact_table_json_records(
    *,
    records: Iterable[Mapping[str, Any]] | None,
    column_keys: tuple[str, ...] | None = None,
    column_definitions: Mapping[str, CompactTableColumnDefinition] | None = None,
    row_key: str | None = None,
    row_header_key: str | None = None,
    row_header_label: DisplayValue | None = None,
    section_key: str | None = None,
    span_rows_when_only_row_header: bool = False,
    show_header: bool = True,
    class_name: str = '',
    wrapper_class_name: str = '',
    emphasized: bool = True,
) -> CompactTableData:
    normalized_records = _normalize_records(records=records)
    resolved_column_keys = _resolve_column_keys(
        records=normalized_records,
        column_keys=column_keys,
        column_definitions=column_definitions,
    )
    resolved_row_header_key = row_header_key
    if resolved_row_header_key is None and resolved_column_keys:
        resolved_row_header_key = resolved_column_keys[0]

    columns = _build_json_columns(
        column_keys=resolved_column_keys,
        column_definitions=column_definitions or {},
        row_header_key=resolved_row_header_key,
        row_header_label=row_header_label,
    )

    return CompactTableData(
        columns=_map_columns(
            definitions=columns,
        ),
        rows=tuple(
            _map_json_record_row(
                record=record,
                column_keys=resolved_column_keys,
                row_index=index,
                row_key=row_key,
                row_header_key=resolved_row_header_key,
                section_key=section_key,
                span_rows_when_only_row_header=span_rows_when_only_row_header,
            )
            for index, record in enumerate(normalized_records)
        ),
        show_header=show_header,
        class_name=class_name,
        wrapper_class_name=wrapper_class_name,
        emphasized=emphasized,
    )


def map_compact_table_row(
    *,
    definition: CompactTableRowDefinition,
    kpis: Mapping[str, Any],
    row_index: int = 0,
) -> CompactTableRowData:
    row_key = _resolve_row_key(
        definition=definition,
        kpis=kpis,
        row_index=row_index,
    )

    is_span = _resolve_bool(
        value=definition.is_span,
        key=definition.is_span_key,
        kpis=kpis,
    )

    row_color = _resolve_value(
        definition=definition.color,
        kpis=kpis,
    )

    row_class_name = _resolve_class_name(
        class_name=definition.class_name,
        class_name_key=definition.class_name_key,
        kpis=kpis,
    )

    row_emphasized = _resolve_bool(
        value=definition.emphasized,
        key=definition.emphasized_key,
        kpis=kpis,
    )

    if is_span:
        return CompactTableRowData.span(
            key=row_key,
            value=_resolve_value(
                definition=definition.span_value,
                kpis=kpis,
            ),
            color=row_color,
            class_name=row_class_name,
            emphasized=row_emphasized,
        )

    return CompactTableRowData.data(
        key=row_key,
        cells={
            column_key: map_compact_table_cell(
                definition=cell_definition,
                kpis=kpis,
            )
            for column_key, cell_definition in definition.cells.items()
        },
        color=row_color,
        class_name=row_class_name,
        emphasized=row_emphasized,
        first_cell_marker=_resolve_bool(
            value=definition.first_cell_marker,
            key=definition.first_cell_marker_key,
            kpis=kpis,
        ),
    )


def map_compact_table_cell(
    *,
    definition: CompactTableCellDefinition,
    kpis: Mapping[str, Any],
) -> CompactTableCellData:
    title = _resolve_value(
        definition=definition.title,
        kpis=kpis,
    )

    return CompactTableCellData(
        value=_resolve_value(
            definition=definition.value,
            kpis=kpis,
        ),
        color=_resolve_value(
            definition=definition.color,
            kpis=kpis,
        ),
        align=definition.align,
        class_name=_resolve_class_name(
            class_name=definition.class_name,
            class_name_key=definition.class_name_key,
            kpis=kpis,
        ),
        emphasized=_resolve_bool(
            value=definition.emphasized,
            key=definition.emphasized_key,
            kpis=kpis,
        ),
        title=str(title) if title is not None else None,
    )



class _JsonSourceDefault:
    def __init__(self, value: Any) -> None:
        self.value = value


def _resolve_json_source_records(
    *,
    source: CompactTableJsonRecordsSource,
    kpis: Mapping[str, Any],
) -> Iterable[Mapping[str, Any]] | _JsonSourceDefault:
    source_value = _read_key(
        source=kpis,
        key=source.kpi_key,
        default=None,
    )

    if isinstance(source_value, Mapping):
        if 'is_ok' in source_value or 'payload' in source_value or 'default' in source_value:
            if source_value.get('is_ok') is False:
                return _JsonSourceDefault(source_value.get('default'))

            payload = source_value.get('payload')
            if source.records_key and isinstance(payload, Mapping):
                payload = _read_key(
                    source=payload,
                    key=source.records_key,
                    default=None,
                )
            return _normalize_json_payload(payload)

        if source_value.get('status') and source_value.get('value_kind'):
            status = str(source_value.get('status'))
            if status != 'ok':
                return _JsonSourceDefault(None)

            if source_value.get('value_kind') != 'json':
                return _JsonSourceDefault(None)

            payload = source_value.get('value')
            if source.records_key and isinstance(payload, Mapping):
                payload = _read_key(
                    source=payload,
                    key=source.records_key,
                    default=None,
                )
            return _normalize_json_payload(payload)

        if source.records_key:
            payload = _read_key(
                source=source_value,
                key=source.records_key,
                default=None,
            )
            return _normalize_json_payload(payload)

    return _normalize_json_payload(source_value)


def _normalize_json_payload(value: Any) -> tuple[Mapping[str, Any], ...]:
    if value is None:
        return ()

    if isinstance(value, Mapping):
        return (value,)

    if isinstance(value, Iterable) and not isinstance(value, (str, bytes)):
        return tuple(item for item in value if isinstance(item, Mapping))

    return ()

def _map_columns(
    *,
    definitions: tuple[CompactTableColumnDefinition, ...],
) -> tuple[CompactTableColumnData, ...]:
    return tuple(
        CompactTableColumnData(
            key=definition.key,
            label=definition.label,
            align=definition.align,
            header_align=definition.header_align,
            width=definition.width,
            class_name=definition.class_name,
            header_class_name=definition.header_class_name,
            is_row_header=definition.is_row_header,
        )
        for definition in definitions
    )


def _normalize_records(
    *,
    records: Iterable[Mapping[str, Any]] | None,
) -> tuple[Mapping[str, Any], ...]:
    if records is None:
        return ()

    return tuple(record for record in records if isinstance(record, Mapping))


def _resolve_column_keys(
    *,
    records: tuple[Mapping[str, Any], ...],
    column_keys: tuple[str, ...] | None,
    column_definitions: Mapping[str, CompactTableColumnDefinition] | None,
) -> tuple[str, ...]:
    if column_keys:
        return tuple(dict.fromkeys(column_keys))

    keys: list[str] = []

    if column_definitions:
        keys.extend(column_definitions.keys())

    for record in records:
        keys.extend(str(key) for key in record.keys())

    return tuple(dict.fromkeys(keys))


def _build_json_columns(
    *,
    column_keys: tuple[str, ...],
    column_definitions: Mapping[str, CompactTableColumnDefinition],
    row_header_key: str | None,
    row_header_label: DisplayValue | None,
) -> tuple[CompactTableColumnDefinition, ...]:
    columns: list[CompactTableColumnDefinition] = []
    default_width = _resolve_default_width(column_keys=column_keys)

    for key in column_keys:
        column_definition = column_definitions.get(key)
        is_row_header = key == row_header_key
        if column_definition is not None:
            if is_row_header and row_header_label is not None:
                column_definition = CompactTableColumnDefinition(
                    key=column_definition.key,
                    label=row_header_label,
                    align=column_definition.align,
                    header_align=column_definition.header_align,
                    width=column_definition.width,
                    class_name=column_definition.class_name,
                    header_class_name=column_definition.header_class_name,
                    is_row_header=column_definition.is_row_header,
                )
            columns.append(column_definition)
            continue

        columns.append(
            CompactTableColumnDefinition(
                key=key,
                label=(
                    row_header_label
                    if is_row_header and row_header_label is not None
                    else _format_column_label(key)
                ),
                align='start' if is_row_header else 'end',
                width=default_width,
                is_row_header=is_row_header,
            ),
        )

    return tuple(columns)


def _resolve_default_width(*, column_keys: tuple[str, ...]) -> str | None:
    if not column_keys:
        return None

    return f'{round(100 / len(column_keys), 4)}%'


def _format_column_label(key: str) -> str:
    return key.replace('_', ' ').upper()


def _map_json_record_row(
    *,
    record: Mapping[str, Any],
    column_keys: tuple[str, ...],
    row_index: int,
    row_key: str | None,
    row_header_key: str | None,
    section_key: str | None,
    span_rows_when_only_row_header: bool,
) -> CompactTableRowData:
    resolved_row_key = f'compact-table-json-row-{row_index}'
    if row_key:
        value = _read_key(
            source=record,
            key=row_key,
            default=None,
        )
        if value is not None:
            resolved_row_key = str(value)

    section_value = _resolve_json_section_value(
        record=record,
        column_keys=column_keys,
        row_header_key=row_header_key,
        section_key=section_key,
        span_rows_when_only_row_header=span_rows_when_only_row_header,
    )
    if section_value is not None:
        return CompactTableRowData.span(
            key=resolved_row_key,
            value=section_value,
            emphasized=True,
        )

    return CompactTableRowData.data(
        key=resolved_row_key,
        cells={key: record.get(key) for key in column_keys},
    )


def _resolve_json_section_value(
    *,
    record: Mapping[str, Any],
    column_keys: tuple[str, ...],
    row_header_key: str | None,
    section_key: str | None,
    span_rows_when_only_row_header: bool,
) -> Any:
    if section_key:
        section_value = _read_key(
            source=record,
            key=section_key,
            default=None,
        )
        if not _is_empty_value(section_value):
            return section_value

    if not span_rows_when_only_row_header or not row_header_key:
        return None

    row_header_value = _read_key(
        source=record,
        key=row_header_key,
        default=None,
    )
    if _is_empty_value(row_header_value):
        return None

    value_keys = tuple(key for key in column_keys if key != row_header_key)
    if not value_keys:
        return row_header_value

    if all(_is_empty_value(record.get(key)) for key in value_keys):
        return row_header_value

    return None


def _is_empty_value(value: Any) -> bool:
    if value is None:
        return True

    if isinstance(value, str):
        return value.strip() == ''

    return False


def _resolve_value(
    *,
    definition: TableValueDefinition,
    kpis: Mapping[str, Any],
) -> Any:
    if definition.key:
        value = _read_key(
            source=kpis,
            key=definition.key,
            default=definition.default,
        )
    else:
        value = definition.value

    if value is None:
        value = definition.default

    if definition.template and value is not None:
        return definition.template.format(value)

    return value


def _resolve_bool(
    *,
    value: bool,
    key: str | None,
    kpis: Mapping[str, Any],
) -> bool:
    if not key:
        return bool(value)

    return _to_bool(
        _read_key(
            source=kpis,
            key=key,
            default=False,
        ),
    )


def _resolve_row_key(
    *,
    definition: CompactTableRowDefinition,
    kpis: Mapping[str, Any],
    row_index: int,
) -> str:
    if definition.key_key:
        value = _read_key(
            source=kpis,
            key=definition.key_key,
            default=None,
        )

        if value is not None:
            return str(value)

    if definition.key:
        return definition.key

    return f'compact-table-row-{row_index}'


def _resolve_class_name(
    *,
    class_name: str,
    class_name_key: str | None,
    kpis: Mapping[str, Any],
) -> str:
    dynamic_class_name = ''

    if class_name_key:
        dynamic_class_name = str(
            _read_key(
                source=kpis,
                key=class_name_key,
                default='',
            )
            or '',
        )

    return f'{class_name} {dynamic_class_name}'.strip()


def _read_key(
    *,
    source: Mapping[str, Any],
    key: str,
    default: Any = None,
) -> Any:
    current: Any = source

    for key_part in key.split('.'):
        if isinstance(current, Mapping):
            current = current.get(key_part, _MISSING)
        else:
            current = getattr(current, key_part, _MISSING)

        if current is _MISSING:
            return default

    return current


def _to_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value

    if isinstance(value, str):
        return value.strip().lower() in {'1', 'true', 'yes', 'y', 'si', 'sí', 'on'}

    return bool(value)
