from __future__ import annotations

from ..components.vertimil.definition import VertimilDefinition
from ..components.bomba.definition import BombasGroupDefinition, BombaDefinition, PositionList

def _build_vertimil_definition(*, vertimil_number: str) -> VertimilDefinition:
    return VertimilDefinition(
        label=f'VT-{vertimil_number}',
        vertimil_state_key=f'estado_vertimil_{vertimil_number}_inst',
        vertimil_value_key=f'amperaje_vertimil_{vertimil_number}_inst',
        vertimil_color_key='',
        vertimil_unit='A'
    )

VERTIMILS_DEFINITION: tuple[VertimilDefinition, ...] = (
    _build_vertimil_definition(vertimil_number='009'),
    _build_vertimil_definition(vertimil_number='010'),
    _build_vertimil_definition(vertimil_number='701'),
)

BOMBAS_DEFINITION: BombasGroupDefinition = BombasGroupDefinition(
    bombas_group=(
        {
            'vertical': (
                BombaDefinition(label='PP45', bomba_state_key='estado_bomba045_inst'),
                BombaDefinition(label='PP46', bomba_state_key='estado_bomba046_inst'),
            )
        },
        {
            'vertical': (
                BombaDefinition(label='PP52', bomba_state_key='estado_bomba052_inst'),
                BombaDefinition(label='PP53', bomba_state_key='estado_bomba053_inst'),
            )
        },
        {
            'vertical': (
                BombaDefinition(label='PP855', bomba_state_key='estado_bomba855_inst'),
                BombaDefinition(label='PP856', bomba_state_key='estado_bomba856_inst'),
            )
        }
    )
)