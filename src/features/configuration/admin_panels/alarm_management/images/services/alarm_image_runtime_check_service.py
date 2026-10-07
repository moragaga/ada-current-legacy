from __future__ import annotations

import random
from datetime import UTC, datetime, timedelta

from ..models.alarm_image_runtime_state import AlarmImageRuntimeState


class AlarmImageRuntimeCheckService:
    def __init__(
        self,
        *,
        success_interval_seconds: int = 180,
        failure_interval_seconds: int = 60,
        jitter_seconds: int = 60,
    ) -> None:
        self._success_interval_seconds = success_interval_seconds
        self._failure_interval_seconds = failure_interval_seconds
        self._jitter_seconds = jitter_seconds

    @staticmethod
    def should_check(
        *,
        state: AlarmImageRuntimeState,
        force: bool = False,
    ) -> bool:
        if force:
            return True

        if not state.next_check_at:
            return True

        try:
            next_check_at = datetime.fromisoformat(state.next_check_at)
        except ValueError:
            return True

        return datetime.now(UTC) >= next_check_at

    def schedule_success(self, state: AlarmImageRuntimeState) -> AlarmImageRuntimeState:
        now = datetime.now(UTC)
        state.last_check_at = now.isoformat()
        state.last_success_at = now.isoformat()
        state.last_error = None
        state.next_check_at = (
            now + timedelta(seconds=self._success_interval_seconds + self._jitter())
        ).isoformat()
        return state

    def schedule_failure(
        self,
        *,
        state: AlarmImageRuntimeState,
        error: str,
    ) -> AlarmImageRuntimeState:
        now = datetime.now(UTC)
        state.last_check_at = now.isoformat()
        state.last_failure_at = now.isoformat()
        state.last_error = error
        state.next_check_at = (
            now + timedelta(seconds=self._failure_interval_seconds + self._jitter())
        ).isoformat()
        return state

    def _jitter(self) -> int:
        if self._jitter_seconds <= 0:
            return 0

        return random.randint(0, self._jitter_seconds)
