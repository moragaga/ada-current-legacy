from __future__ import annotations

from src.shared.ui.components.compact_table import (
    CompactTableColumnDefinition,
    CompactTableDefinition,
    CompactTableJsonRecordsSource,
)

GESTION_CARGUIO_TURNO_DEFINITION = CompactTableDefinition(
    columns=(
        CompactTableColumnDefinition(
            key='equipo',
            label='',
            align='start',
            width='8%',
            is_row_header=False,
        ),
        CompactTableColumnDefinition(
            key='fase',
            label='FASE',
            width='8%',
            align='end',
        ),
        CompactTableColumnDefinition(
            key='uebd_pct',
            label='UEBD (%)',
            width='9%',
            align='end',
        ),
        CompactTableColumnDefinition(
            key='disponibilidad_fisica_pct',
            label='Disponibilidad (%)',
            width='15.5%',
            align='end',
        ),
        CompactTableColumnDefinition(
            key='rendimiento_efectivo_tph',
            label='Rendimiento (t/hr)',
            width='15.5%',
            align='end',
        ),
        CompactTableColumnDefinition(
            key='cola_pala_min',
            label='T.Cola (min)',
            width='11%',
            align='end',
        ),
        CompactTableColumnDefinition(
            key='estado',
            label='Estado',
            align='end',
            width='7%',
        ),
        CompactTableColumnDefinition(
            key='razon',
            label='Razón',
            align='end',
            width='26%',
        ),
    ),
    json_records_source=CompactTableJsonRecordsSource(
        kpi_key='carguio_tiempos_colas_turno_inst',
        row_key='row_id',
        row_header_key='equipo',
        row_header_label='',
        span_rows_when_only_row_header=True,
    ),
)