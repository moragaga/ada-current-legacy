from __future__ import annotations

from src.shared.ui.rendering import KpiBuildDefinition

from .content.colectiva import build_colectiva_content
from .content.selectiva import build_selectiva_content

CONTENT_BUILDER_DEFINITION = [
    KpiBuildDefinition(
        slot_name='FLOTACIÓN - COLECTIVA',
        builder=build_colectiva_content,
        ui_size='large',
        exclude_parameters=('timestamps', 'timeseries'),
    ),
    KpiBuildDefinition(
        slot_name='FLOTACIÓN - SELECTIVA',
        builder=build_selectiva_content,
        ui_size='large',
        exclude_parameters=('timestamps', 'timeseries'),
    ),
]
