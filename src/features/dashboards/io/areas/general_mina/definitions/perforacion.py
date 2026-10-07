from __future__ import annotations

from src.shared.ui.components.compact_table import (
    CompactTableColumnDefinition,
    CompactTableDefinition,
    CompactTableJsonRecordsSource,
)

PERFORACION_SUMMARY_DEFINITION: CompactTableDefinition = CompactTableDefinition(
    columns=(
        CompactTableColumnDefinition(
            key='fase',
            label='Fase',
            align='start',
            width='16%',
            is_row_header=True,
        ),
        CompactTableColumnDefinition(
            key='perforadora',
            label='Perfo. (m)',
            align='start',
            width='22%',
        ),
        CompactTableColumnDefinition(
            key='t_anterior',
            label='T. Anterior (m)',
            align='end',
            width='31%',
        ),
        CompactTableColumnDefinition(
            key='acum_semana',
            label='Acum. Semana (m)',
            align='end',
            width='31%',
        ),
    ),
    json_records_source=CompactTableJsonRecordsSource(
        kpi_key='perforacion_summary_inst',
        row_key='perforadora',
        row_header_key='fase',
        row_header_label='Fase',
        span_rows_when_only_row_header=True,
    ),
)