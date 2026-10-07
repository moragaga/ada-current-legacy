from __future__ import annotations

from dataclasses import dataclass
from typing import TypeAlias

from src.shared.ui.components.metrics import StandardMetricDefinition

DisplayKey: TypeAlias = str | None


@dataclass(frozen=True, slots=True)
class CorreaStmgDefinition:
    label: str
    correa_state_key: DisplayKey = None


@dataclass(frozen=True, slots=True)
class CorreaStmgGroupDefinition:
    correas: tuple[CorreaStmgDefinition, ...]
    metrics: tuple[StandardMetricDefinition, ...] = None
