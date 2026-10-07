from __future__ import annotations

from src.shared.ui.display.slot_container import (
    build_slot_container,
    build_slot_ready_flag_container,
)

from ..ids import PuertoIds


def build_desaladora_container():
    return build_slot_container(component_id=PuertoIds.DESALADORA, class_name='')


def build_puerto_container():
    return build_slot_container(component_id=PuertoIds.PUERTO, class_name='')


def build_puerto_ready_flag():
    return build_slot_ready_flag_container(id_flag=PuertoIds.READY_FLAG)
