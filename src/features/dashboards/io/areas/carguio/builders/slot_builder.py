from __future__ import annotations

from src.shared.ui.display.slot_container import (
    build_slot_container,
    build_slot_ready_flag_container,
)

from ..ids import CarguioIds


def build_equipos_servicio_container():
    return build_slot_container(component_id=CarguioIds.EQUIPOS_SERVICIO, class_name='')


def build_mezcla_container():
    return build_slot_container(component_id=CarguioIds.MEZCLA, class_name='')


def build_carguio_ready_flag():
    return build_slot_ready_flag_container(id_flag=CarguioIds.READY_FLAG)
