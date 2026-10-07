from __future__ import annotations

from typing import Any

from ..models.mp10 import MP10Data


def build_mp10_mapper(*, kpis: dict[str, Any]) -> MP10Data:
    return MP10Data.from_kpis(kpis=kpis)
