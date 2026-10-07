from __future__ import annotations

from src.shared.ui.components.metrics import DualMetricDefinition

_FS_COLUMN = 'fs-io-200'

TIEMPOS_COLAS_TURNO_DEFINITION: tuple[DualMetricDefinition, ...] = (
    DualMetricDefinition(
        label='Cola Chancado',
        first_kpi_key='',
        first_unit="'",
        first_color_key='',
        divider_value='·',
        second_kpi_key='',
        second_unit='CAEX',
        second_color_key='',
        font_size_class_name=_FS_COLUMN,
    ),
    DualMetricDefinition(
        label='Cola Palas',
        first_kpi_key='',
        first_unit="'",
        first_color_key='',
        divider_value='·',
        second_kpi_key='',
        second_unit='CAEX',
        second_color_key='',
        font_size_class_name=_FS_COLUMN,
    ),
    DualMetricDefinition(
        label='Esp. Mineral',
        first_kpi_key='',
        first_unit="'",
        first_color_key='',
        divider_value='·',
        second_kpi_key='',
        second_unit='CAEX',
        second_color_key='',
        font_size_class_name=_FS_COLUMN,
    ),
    DualMetricDefinition(
        label='Desc. Chancado',
        first_kpi_key='',
        first_unit="'",
        first_color_key='',
        divider_value='·',
        second_kpi_key='',
        second_color_key='',
        font_size_class_name=_FS_COLUMN,
    ),
)
