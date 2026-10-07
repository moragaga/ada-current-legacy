from __future__ import annotations

from dataclasses import dataclass

from .models import GaugeVariant


@dataclass(frozen=True, slots=True)
class LevelGaugeDefinition:
    number: str
    variant: GaugeVariant
    image_name: str
    name_prefix: str
    tag_prefix: str
    unit: str = '%'
    percentage_key_suffix: str = 'nivel_inst'
    state_key_suffix: str = 'estado_inst'
    color_key_suffix: str = 'nivel_color'

    @property
    def name(self) -> str:
        return f'{self.name_prefix}-{self.number}'

    @property
    def percentage_kpi_key(self) -> str:
        return f'nivel_{self.tag_prefix}_0{self.number}_inst'

    @property
    def state_kpi_key(self) -> str:
        return f'estado_{self.tag_prefix}_0{self.number}_inst'

    @property
    def color_kpi_key(self) -> str:
        return f'{self.tag_prefix}{self.number}_{self.color_key_suffix}'

    @property
    def trigger_graph_key(self) -> str:
        return f'{self.tag_prefix}{self.number}_trigger_id'
