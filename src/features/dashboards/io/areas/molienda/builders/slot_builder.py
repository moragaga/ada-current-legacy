from __future__ import annotations

from src.shared.ui.display.slot_container import (
    build_slot_container,
    build_slot_ready_flag_container,
)

from ..ids import MoliendaIds


def build_molienda_container():
    return build_slot_container(component_id=MoliendaIds.MOLIENDA, class_name='')


def build_molienda_ready_flag():
    return build_slot_ready_flag_container(id_flag=MoliendaIds.READY_FLAG)
