from __future__ import annotations

from src.shared.ui.rendering import KpiBuildDefinition

from .content.chancado_stmg import build_chancado_stmg_content

CONTENT_BUILDER_DEFINITION = [
    KpiBuildDefinition(
        slot_name='CHANCADO & STMG - CHANCADO & STMG',
        builder=build_chancado_stmg_content,
        ui_size='large',
        exclude_parameters=('timestamps', 'timeseries'),
    ),
]
