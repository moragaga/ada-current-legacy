from __future__ import annotations

from src.shared.ui.rendering import KpiBuildDefinition

from .content.molienda import build_molienda_content

CONTENT_BUILDER_DEFINITION = [
    KpiBuildDefinition(
        slot_name='MOLIENDA - MOLIENDA',
        builder=build_molienda_content,
        ui_size='large',
        exclude_parameters=('timestamps', 'timeseries'),
    ),
]
