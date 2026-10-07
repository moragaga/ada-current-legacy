from __future__ import annotations

from src.shared.ui.rendering import KpiBuildDefinition

from .content.equipos_servicio import (
    build_equipos_servicio_content,
    build_equipos_servicio_total,
)
from .content.mezcla import build_mezcla_content

CONTENT_BUILDER_DEFINITION = [
    # Arriba: MEZCLA
    KpiBuildDefinition(
        slot_name='CARGUÍO - EQUIPOS DE SERVICIO',
        builder=build_mezcla_content,
        ui_size='large',
        exclude_parameters=('timestamps', 'timeseries'),
    ),
    # Abajo: EQUIPOS DE SERVICIO (como CompactTable con valor / plan)
    KpiBuildDefinition(
        slot_name='CARGUÍO - MEZCLA',
        builder=build_equipos_servicio_content,
        ui_size='large',
        exclude_parameters=('timestamps', 'timeseries'),
    ),
    KpiBuildDefinition(
        slot_name='CARGUIO - EQUIPOS DE SERVICIO TOTAL',
        builder=build_equipos_servicio_total,
        ui_size='small',
        exclude_parameters=('timestamps', 'timeseries'),
    ),
]