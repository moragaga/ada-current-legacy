from __future__ import annotations

from src.shared.ui.components.compact_table import (
    CompactTableColumnDefinition,
    CompactTableDefinition,
    CompactTableJsonRecordsSource,
)

MOVIMIENTO_MINA_SUMMARY_DEFINITION: CompactTableDefinition = CompactTableDefinition(
    columns=(
        CompactTableColumnDefinition(
            key='label',
            label='',
            align='start',
            width='36%',
            is_row_header=True,
        ),
        CompactTableColumnDefinition(
            key='real',
            label='Real Día',
            align='end',
            width='12%',
        ),
        CompactTableColumnDefinition(
            key='plan',
            label='Plan Acumulado',
            align='end',
            width='12%',
        ),
        CompactTableColumnDefinition(
            key='proyeccion',
            label='Proyección',
            align='end',
            width='14%',
        ),
        CompactTableColumnDefinition(
            key='objetivo_dia',
            label='Plan',
            align='end',
            width='13%',
        ),
        CompactTableColumnDefinition(
            key='requerido',
            label='Requerido',
            align='end',
            width='13%',
        ),
    ),
    json_records_source=CompactTableJsonRecordsSource(
        kpi_key='movimiento_mina_summary_inst',
        row_key='label',
        row_header_key='label',
        row_header_label='',
    ),
)
