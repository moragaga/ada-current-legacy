from __future__ import annotations

from ..components.molino_bolas.definition import MolinoBolasDefinition

def _build_molino_bolas_definition(*, mb_number: int, sag_number: int) -> MolinoBolasDefinition:
    compose_number = f'00{mb_number}' if mb_number < 10 else f'0{mb_number}'
    return MolinoBolasDefinition(
        label=f'MB-{compose_number}',
        mb_state_key=f'estado_mb{compose_number}_sag_{sag_number}_inst',
        mb_power_key=f'potencia_mb{compose_number}_sag_{sag_number}_inst',
        mb_power_color_key=f'potencia_mb{compose_number}_sag_{sag_number}_color_inst',
    )

MB_SAG_1_DEFINITION: tuple[MolinoBolasDefinition, ...] = (
    _build_molino_bolas_definition(mb_number=4, sag_number=1),
    _build_molino_bolas_definition(mb_number=5, sag_number=1),
)
MB_SAG_2_DEFINITION: tuple[MolinoBolasDefinition, ...] = (
    _build_molino_bolas_definition(mb_number=6, sag_number=2),
    _build_molino_bolas_definition(mb_number=7, sag_number=2),
)
MB_SAG_3_DEFINITION: tuple[MolinoBolasDefinition, ...] = (
    _build_molino_bolas_definition(mb_number=8, sag_number=3),
    _build_molino_bolas_definition(mb_number=9, sag_number=3),
)
MB_SAG_4_DEFINITION: tuple[MolinoBolasDefinition, ...] = (
    _build_molino_bolas_definition(mb_number=10, sag_number=4),
)
