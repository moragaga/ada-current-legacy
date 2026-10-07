from __future__ import annotations

from src.shared.ui.components.metrics import StandardMetricDefinition

_FS_COLUMN = 'fs-io-200'

NO_OPERATIVO_TURNO_DEFINITION: tuple[StandardMetricDefinition, ...] = (
    StandardMetricDefinition(
        label='Efectivos',
        kpi_key='numero_caex_total_real_inst',
        color_key='',
        font_size_class_name=_FS_COLUMN,
    ),
    StandardMetricDefinition(
        label='Mantención',
        kpi_key='caex_fuera_servicio_inst',
        color_key='',
        font_size_class_name=_FS_COLUMN,
    ),
    StandardMetricDefinition(
        label='Demora',
        kpi_key='caex_demora_inst',
        color_key='',
        font_size_class_name=_FS_COLUMN,
    ),
    StandardMetricDefinition(
        label='Reserva',
        kpi_key='caex_reserva_inst',
        color_key='',
        font_size_class_name=_FS_COLUMN,
    ),
)
