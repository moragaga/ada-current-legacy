from __future__ import annotations

from dataclasses import dataclass
from typing import TypeAlias

DisplayKey: TypeAlias = str | None


@dataclass(frozen=True, slots=True)
class StockpileMinaDetailDefinition:
    percentage_key: DisplayKey
    meters_key: DisplayKey


@dataclass(frozen=True, slots=True)
class StockpileMinaDefinition:
    piles: tuple[StockpileMinaDetailDefinition, ...]
