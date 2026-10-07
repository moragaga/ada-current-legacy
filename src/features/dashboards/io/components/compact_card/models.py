from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, TypeAlias

from dash.development.base_component import Component

from .builds import (
    build_compact_card_component,
    build_compact_card_group_component,
    build_compact_card_row_component,
)

DisplayValue: TypeAlias = str | int | float | Component | None
IndicatorPosition: TypeAlias = str


@dataclass(frozen=True, slots=True)
class CompactCardTitleData:
    label: str
    label_class_name: str = ''
    extra_label: str | None = None
    extra_label_class_name: str = ''


@dataclass(frozen=True, slots=True)
class CompactCardValueData:
    label: str
    label_class_name: str = ''
    value: DisplayValue = None
    value_class_name: str = ''
    color: DisplayValue = None


@dataclass(frozen=True, slots=True)
class CompactCardData:
    title: CompactCardTitleData
    values: tuple[CompactCardValueData, ...]
    card_color: DisplayValue = None
    wrapper_class_name: str | None = 'compact-card-span-color'

    def to_component(self) -> Component:
        return build_compact_card_component(model=self)


@dataclass(frozen=True, slots=True)
class CompactCardGroupData:
    cards: tuple[CompactCardData, ...]
    indicator: str | None = None
    indicator_position: IndicatorPosition = 'top'
    wrapper_class_name: str | None = None

    @classmethod
    def from_iterable(
        cls,
        *,
        cards: Iterable[CompactCardData],
        indicator: str | None = None,
        indicator_position: IndicatorPosition = 'top',
        wrapper_class_name: str | None = None,
    ) -> CompactCardGroupData:
        return cls(
            cards=tuple(cards),
            indicator=indicator,
            indicator_position=indicator_position,
            wrapper_class_name=wrapper_class_name,
        )

    def to_component(self) -> Component:
        return build_compact_card_group_component(model=self)

    def __iter__(self) -> Iterable[CompactCardData]:
        return iter(self.cards)

    def __len__(self) -> int:
        return len(self.cards)


@dataclass(frozen=True, slots=True)
class CompactCardRowData:
    rows: tuple[CompactCardGroupData, ...]

    def to_component(self) -> Component:
        return build_compact_card_row_component(model=self)
