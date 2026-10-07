from __future__ import annotations

from src.shared.ui.display.slot_container import (
    build_slot_container,
    build_slot_ready_flag_container,
)

from ..ids import FlotacionIds


def build_colectiva_container():
    return build_slot_container(component_id=FlotacionIds.COLECTIVA, class_name='')


def build_selectiva_container():
    return build_slot_container(component_id=FlotacionIds.SELECTIVA, class_name='')


def build_flotacion_ready_flag():
    return build_slot_ready_flag_container(id_flag=FlotacionIds.READY_FLAG)
