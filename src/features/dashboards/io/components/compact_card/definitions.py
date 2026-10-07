from __future__ import annotations

from dataclasses import dataclass
from typing import TypeAlias

DisplayKey: TypeAlias = str | None
IndicatorPosition: TypeAlias = str


@dataclass(frozen=True, slots=True)
class CompactCardTitleDefinition:
    label: str
    label_class_name: str = ''
    extra_label: str | None = None
    extra_label_class_name: str = ''


@dataclass(frozen=True, slots=True)
class CompactCardValueDefinition:
    label: str
    label_class_name: str = ''
    value_key: DisplayKey = None
    value_class_name: str = ''
    color_key: DisplayKey = None


@dataclass(frozen=True, slots=True)
class CompactCardDefinition:
    title: CompactCardTitleDefinition
    values: tuple[CompactCardValueDefinition, ...]
    card_color_key: DisplayKey = None
    wrapper_class_name: str | None = 'compact-card-span-color'


@dataclass(frozen=True, slots=True)
class CompactCardGroupDefinition:
    cards: tuple[CompactCardDefinition, ...]
    indicator: str | None = None
    indicator_position: IndicatorPosition = 'top'
    wrapper_class_name: str | None = None


@dataclass(frozen=True, slots=True)
class CompactCardRowDefinition:
    rows: tuple[CompactCardGroupDefinition, ...]
