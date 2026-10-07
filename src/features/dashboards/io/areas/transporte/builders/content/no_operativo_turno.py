from __future__ import annotations

from ...mappers.no_operativo_turno import build_no_operativo_turno_mapper

def build_no_operativo_turno_content(kpis: dict) -> list:
    return build_no_operativo_turno_mapper(kpis=kpis).to_components()