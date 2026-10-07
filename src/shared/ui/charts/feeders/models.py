from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, TypeAlias

from dash.development.base_component import Component

from .build import build_feeders_chart

DisplayValue: TypeAlias = str | None | Component


@dataclass(frozen=True, slots=True)
class FeederData:
    label: str
    value: DisplayValue = None
    color: DisplayValue = None


@dataclass(frozen=True, slots=True)
class FeedersData:
    feeders: tuple[FeederData, ...]

    @classmethod
    def from_iterable(cls, items: Iterable[FeederData]) -> FeedersData:
        return cls(feeders=tuple(items))

    def to_component(self) -> Component:
        return build_feeders_chart(model=self)

    def __iter__(self) -> Iterable[FeederData]:
        return iter(self.feeders)

    def __len__(self) -> int:
        return len(self.feeders)
