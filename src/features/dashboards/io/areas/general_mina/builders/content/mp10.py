from __future__ import annotations

from ...components.mp10_component import build_mp10_component
from ...mappers.mp10 import build_mp10_mapper


def build_mp10_content(kpis: dict):
    return build_mp10_component(model=build_mp10_mapper(kpis=kpis))
