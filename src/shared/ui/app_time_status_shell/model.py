from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Any

from dash.development.base_component import Component
from .build import build_time_status_indicator, build_time_status_indicator_group

@dataclass(frozen=True, slots=True)
class AppTimeStatusShellStructure:
    label: str
    icon_class_name: str
    value_id: str | None = None
    icon_id: str | None = None
    right_divisor: bool = False
    value: Any | None = None
    wrapper_class_name: str | None = None

    def to_component(self):
        return build_time_status_indicator(definition=self)

@dataclass(frozen=True, slots=True)
class AppTimeStatusShellGroupStructure:
    statuses_structure: tuple[AppTimeStatusShellStructure, ...]

    @classmethod
    def from_iterable(cls, statuses_structure: Iterable[AppTimeStatusShellStructure]) -> AppTimeStatusShellGroupStructure:
        return cls(statuses_structure=tuple(statuses_structure))

    def to_component(self) -> Component:
        return build_time_status_indicator_group(definitions=self)

    def to_components(self) -> list[Component]:
        return [status_structure.to_component() for status_structure in self.statuses_structure]

    def __iter__(self):
        return iter(self.statuses_structure)

    def __len__(self):
        return len(self.statuses_structure)