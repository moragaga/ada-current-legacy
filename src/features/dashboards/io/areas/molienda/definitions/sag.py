from __future__ import annotations

from ..components.sag.definition import SagDefinition

def _build_sag_definition(*, sag_number: int) -> SagDefinition:
    return SagDefinition(
        label=f'SAG {sag_number}',
        sag_state_key=f'estado_sag_{sag_number}_inst',
        sag_power_key=f'potencia_sag_{sag_number}_inst',
        sag_power_color_key=f'estado_sag_{sag_number}_color_inst',
    )

SAG_1_DEFINITION: SagDefinition = _build_sag_definition(sag_number=1)
SAG_2_DEFINITION: SagDefinition = _build_sag_definition(sag_number=2)
SAG_3_DEFINITION: SagDefinition = _build_sag_definition(sag_number=3)
SAG_4_DEFINITION: SagDefinition = _build_sag_definition(sag_number=4)


