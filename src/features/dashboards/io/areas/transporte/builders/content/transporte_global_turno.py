from __future__ import annotations

from ...mappers.transporte_global_turno import build_transporte_global_turno_mapper


def build_transporte_global_turno_content(kpis: dict) -> list:
    return build_transporte_global_turno_mapper(kpis=kpis).to_components()
