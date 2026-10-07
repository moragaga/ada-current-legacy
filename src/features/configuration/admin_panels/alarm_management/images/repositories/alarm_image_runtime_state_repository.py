from __future__ import annotations

import json
import os
from pathlib import Path

from ..models.alarm_image_runtime_state import AlarmImageRuntimeState


class AlarmImageRuntimeStateRepository:
    def __init__(
        self,
        *,
        runtime_root: Path | None = None,
    ) -> None:
        self._runtime_root = runtime_root or Path(
            os.getenv(
                'MANAGED_ALARM_IMAGE_RUNTIME_ROOT',
                'runtime_cache/managed_alarm_images',
            )
        )
        self._state_path = self._runtime_root / 'state.json'

    @property
    def runtime_root(self) -> Path:
        self._runtime_root.mkdir(parents=True, exist_ok=True)
        return self._runtime_root

    def load_state(self) -> AlarmImageRuntimeState:
        if not self._state_path.exists():
            return AlarmImageRuntimeState()

        try:
            data = json.loads(self._state_path.read_text(encoding='utf-8'))
        except json.JSONDecodeError, OSError:
            return AlarmImageRuntimeState()

        if not isinstance(data, dict):
            return AlarmImageRuntimeState()

        return AlarmImageRuntimeState.from_dict(data)

    def save_state(self, state: AlarmImageRuntimeState) -> None:
        self._runtime_root.mkdir(parents=True, exist_ok=True)

        tmp_path = self._state_path.with_suffix('.tmp')
        tmp_path.write_text(
            json.dumps(
                state.to_dict(),
                ensure_ascii=False,
                indent=2,
            ),
            encoding='utf-8',
        )
        tmp_path.replace(self._state_path)
