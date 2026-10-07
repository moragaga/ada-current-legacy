from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, TypeAlias

from dash.development.base_component import Component

from .build import build_stockpile_mina_chart

DisplayValue: TypeAlias = str | None | Component


@dataclass(frozen=True, slots=True)
class StockpileMinaDetailData:
    percentage_value: DisplayValue
    meters_value: DisplayValue
    percentage_unit: str = '%'
    meters_unit: str = 'm'


@dataclass(frozen=True, slots=True)
class StockpileMinaData:
    piles: tuple[StockpileMinaDetailData, ...] = ()

    @classmethod
    def from_data(cls, items: Iterable[StockpileMinaDetailData]) -> StockpileMinaData:
        return cls(piles=tuple(items))

    def to_component(self) -> Component:
        return build_stockpile_mina_chart(model=self)

    def __iter__(self) -> Iterable[StockpileMinaDetailData]:
        return iter(self.piles)

    def __len__(self) -> int:
        return len(self.piles)
