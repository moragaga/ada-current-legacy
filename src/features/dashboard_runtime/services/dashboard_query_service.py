from __future__ import annotations

from typing import Any

from src.shared.ui.status import resolve_latest_value_display
from ..repositories.dashboard_snapshot_repository import DashboardSnapshotRepository


class DashboardQueryService:
    def __init__(
        self,
        snapshot_repository: DashboardSnapshotRepository,
    ) -> None:
        self._snapshot_repository = snapshot_repository

    def get_latest_snapshot(self) -> dict[str, Any] | None:
        return self._snapshot_repository.get_latest_snapshot()

    def get_latest_update(self) -> str:
        data = self._snapshot_repository.get_latest_update() or {}
        data = {key: resolve_latest_value_display(**value) for key, value in data.items()}
        return data
