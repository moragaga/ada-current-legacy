from __future__ import annotations

from src.shared.ui.rendering import KpiBuildDefinition

from .content.movimiento_mina import build_movimiento_mina_content
from .content.mp10 import build_mp10_content
from .content.perforacion import build_perforacion_content
from .content.remanentes import build_remanentes_content

CONTENT_BUILDER_DEFINITION = [
    KpiBuildDefinition(
        slot_name='GENERAL MINA - MOVIMIENTO MINA',
        builder=build_movimiento_mina_content,
        ui_size='large',
        exclude_parameters=('timestamps', 'timeseries'),
    ),
    KpiBuildDefinition(
        slot_name='GENERAL MINA - REMANENTES',
        builder=build_remanentes_content,
        ui_size='large',
        exclude_parameters=('timestamps', 'timeseries'),
    ),
    KpiBuildDefinition(
        slot_name='GENERAL MINA - PERFORACIÓN',
        builder=build_perforacion_content,
        ui_size='large',
        exclude_parameters=('timestamps', 'timeseries'),
    ),
    KpiBuildDefinition(
        slot_name='GENERAL MINA - MP10',
        builder=build_mp10_content,
        ui_size='large',
        exclude_parameters=('timestamps', 'timeseries'),
    ),
]
