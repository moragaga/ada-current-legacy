from __future__ import annotations

from src.shared.ui.rendering import KpiBuildDefinition

from .content.no_operativo_turno import build_no_operativo_turno_content
from .content.tiempo_colas_turno import build_tiempos_colas_turno_content
from .content.transporte_global_turno import build_transporte_global_turno_content

CONTENT_BUILDER_DEFINITION = [
    KpiBuildDefinition(
        slot_name='TRANSPORTE - TRANSPORTE GLOBAL TURNO',
        builder=build_transporte_global_turno_content,
        ui_size='large',
        exclude_parameters=('timestamps', 'timeseries'),
    ),
    KpiBuildDefinition(
        slot_name='TRANSPORTE - NO OPERATIVO TURNO',
        builder=build_no_operativo_turno_content,
        ui_size='large',
        exclude_parameters=('timestamps', 'timeseries'),
    ),
    KpiBuildDefinition(
        slot_name='TRANSPORTE - TIEMPOS DE COLAS TURNO',
        builder=build_tiempos_colas_turno_content,
        ui_size='large',
    ),
]
