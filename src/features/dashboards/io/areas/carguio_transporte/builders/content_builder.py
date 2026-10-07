from __future__ import annotations

from src.shared.ui.rendering import KpiBuildDefinition

from .content.carguio_transporte import build_carguio_transporte_content

CONTENT_BUILDER_DEFINITION = [
    KpiBuildDefinition(
        slot_name='CARGUIO & TRANSPORTE - GESTIÓN CARGUÍO TURNO',
        builder=build_carguio_transporte_content,
        ui_size='large',
        exclude_parameters=('timestamps', 'timeseries'),
    )
]
