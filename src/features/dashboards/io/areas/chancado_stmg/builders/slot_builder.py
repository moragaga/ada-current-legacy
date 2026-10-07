from __future__ import annotations

from src.shared.ui.display.slot_container import (
    build_slot_container,
    build_slot_ready_flag_container,
)

from ..ids import ChancadoSTMGIds


def build_chancado_stmg_container():
    return build_slot_container(component_id=ChancadoSTMGIds.CHANCADO_STMG, class_name='')


def build_chancado_stmg_ready_flag():
    return build_slot_ready_flag_container(id_flag=ChancadoSTMGIds.READY_FLAG)
