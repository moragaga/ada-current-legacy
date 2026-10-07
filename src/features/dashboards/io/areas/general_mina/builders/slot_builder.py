from __future__ import annotations

from src.shared.ui.display.slot_container import (
    build_slot_container,
    build_slot_ready_flag_container,
)

from ..ids import GeneralMinaIds


def build_movimiento_mina_container():
    return build_slot_container(component_id=GeneralMinaIds.MOVIMIENTO_MINA, class_name='')


def build_remanentes_container():
    return build_slot_container(component_id=GeneralMinaIds.REMANENTES, class_name='')


def build_perforacion_container():
    return build_slot_container(component_id=GeneralMinaIds.PERFORACION, class_name='')


def build_mp10_container():
    return build_slot_container(component_id=GeneralMinaIds.MP10, class_name='')


def build_general_mina_ready_flag():
    return build_slot_ready_flag_container(id_flag=GeneralMinaIds.READY_FLAG)
