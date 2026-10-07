from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Literal

Parameters = Literal['kpis', 'timeseries', 'timestamps']


@dataclass(frozen=True, slots=True)
class KpiBuildDefinition:
    slot_name: str
    builder: Callable[..., Any]
    ui_size: str = 'large'
    exclude_parameters: tuple[Parameters, ...] | None = None
    explicit_list: bool = False
