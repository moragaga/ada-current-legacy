from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DashboardShellIODefinition:
    dashboard_interval_ms: int
