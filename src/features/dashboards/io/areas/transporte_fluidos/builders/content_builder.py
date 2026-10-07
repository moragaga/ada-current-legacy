from __future__ import annotations

from src.shared.ui.rendering import KpiBuildDefinition

from .content.str import build_str_content
from .content.stc import build_stc_content
from .content.tranque import build_tranque_content
from .content.sta import build_sta_content

CONTENT_BUILDER_DEFINITION = [
    KpiBuildDefinition(
        slot_name='TRANSPORTE FLUIDOS - STR',
        builder=build_str_content,
        ui_size='large',
        exclude_parameters=('timestamps', 'timeseries'),
    ),
    KpiBuildDefinition(
        slot_name='TRANSPORTE FLUIDOS - STC',
        builder=build_stc_content,
        ui_size='large',
        exclude_parameters=('timestamps', 'timeseries'),
    ),
    KpiBuildDefinition(
        slot_name='TRANSPORTE FLUIDOS - TRANQUE',
        builder=build_tranque_content,
        ui_size='large',
        exclude_parameters=('timestamps', 'timeseries'),
    ),
    KpiBuildDefinition(
        slot_name='TRANSPORTE FLUIDOS - STA',
        builder=build_sta_content,
        ui_size='large',
        exclude_parameters=('timestamps', 'timeseries'),
    ),
]
