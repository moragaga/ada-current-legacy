from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class DashboardRuntimeStoreKind(str, Enum):
    DATA = 'data'
    TIMELINES = 'timelines'
    TIMESTAMPS = 'timestamps'


@dataclass(frozen=True, slots=True)
class DashboardRuntimeStoreSpec:
    component_key: str
    store_id: str
    kind: DashboardRuntimeStoreKind
