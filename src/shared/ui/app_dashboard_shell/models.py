from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DashboardShellDefinition:
    dashboard_interval_ms: int
