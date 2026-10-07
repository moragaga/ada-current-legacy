from __future__ import annotations

from src.shared.ui.rendering import KpiBuildDefinition

from .content.desaladora import build_desaladora_content
from .content.puerto import build_puerto_content

CONTENT_BUILDER_DEFINITION = [
    KpiBuildDefinition(
        slot_name='PUERTO - DESALADORA',
        builder=build_desaladora_content,
        ui_size='large',
        exclude_parameters=('timestamps', 'timeseries'),
    ),
    KpiBuildDefinition(
        slot_name='PUERTO - PUERTO',
        builder=build_puerto_content,
        ui_size='large',
        exclude_parameters=('timestamps', 'timeseries'),
    ),
]
