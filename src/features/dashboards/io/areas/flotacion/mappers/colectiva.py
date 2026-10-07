from __future__ import annotations

from typing import Any

from ..components.bomba.mapper import map_bomba_group
from ..components.bomba.models import BombaGroupData
from ..definitions.colectiva import VERTIMILS_DEFINITION, BOMBAS_DEFINITION
from ..components.vertimil.models import VertimilGroupData
from ..components.vertimil.mapper import map_vertimil_group

def build_vertimil_mapper(*, kpis: dict[str, Any]) -> VertimilGroupData:
    return map_vertimil_group(
        definitions=VERTIMILS_DEFINITION,
        kpis=kpis,
    )

def build_bomba_mapper(*, kpis: dict[str, Any]) -> BombaGroupData:
    return map_bomba_group(
        definitions=BOMBAS_DEFINITION,
        kpis=kpis,
    )
