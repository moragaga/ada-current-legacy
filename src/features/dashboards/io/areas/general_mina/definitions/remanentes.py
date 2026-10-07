from __future__ import annotations

from typing import Any

from src.shared.ui.components.compact_table import (
    CompactTableColumnDefinition,
    CompactTableDefinition,
    CompactTableJsonRecordsSource,
)
from src.shared.ui.components.metrics import StandardMetricDefinition


REMANENTES_SUMMARY_DEFINITION = CompactTableDefinition(
    columns=(
        CompactTableColumnDefinition(
            key='fase',
            label='',
            align='start',
            width='28%',
            is_row_header=True,
        ),
        CompactTableColumnDefinition(
            key='mineral',
            label='MINERAL',
            align='end',
            width='18%',
        ),
        CompactTableColumnDefinition(
            key='esteril',
            label='ESTERIL',
            align='end',
            width='18%',
        ),
        CompactTableColumnDefinition(
            key='baja_ley',
            label='B. LEY',
            align='end',
            width='18%',
        ),
        CompactTableColumnDefinition(
            key='total',
            label='TOT',
            align='end',
            width='18%',
        ),
    ),
    json_records_source=CompactTableJsonRecordsSource(
        kpi_key='remanentes_summary_inst',
        row_key='fase',
        row_header_key='fase',
        row_header_label='',
    ),
)


REMANENTES_METRIC_DEFINITION: tuple[StandardMetricDefinition, ...] = (
    StandardMetricDefinition(
        label='Stock 3080',
        kpi_key='stock_3080_inst',
        color_key='',
        unit='kt',
        font_size_class_name='fs-io-200',
        container_class_name='app-border-bottom w-100',
    ),
)