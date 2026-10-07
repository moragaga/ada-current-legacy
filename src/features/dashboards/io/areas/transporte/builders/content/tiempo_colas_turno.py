from __future__ import annotations

from ...mappers.tiempo_colas_turno import build_no_operativo_turno_mapper


def build_tiempos_colas_turno_content(kpis: dict) -> list:
    return build_no_operativo_turno_mapper(kpis=kpis).to_components()
