from __future__ import annotations

from dataclasses import dataclass
from typing import TypeAlias

DisplayKey: TypeAlias = str | None


@dataclass(frozen=True, slots=True)
class FeederDefinition:
    label: str
    value_key: DisplayKey = None
    color_key: DisplayKey = None


@dataclass(frozen=True, slots=True)
class FeedersDefinition:
    feeders: tuple[FeederDefinition, ...]
