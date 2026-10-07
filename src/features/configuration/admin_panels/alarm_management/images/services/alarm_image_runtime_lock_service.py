from __future__ import annotations

import json
import os
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Iterator
from uuid import uuid4


@dataclass(slots=True)
class AlarmImageRuntimeLock:
    owner: str


class AlarmImageRuntimeLockService:
    def __init__(
        self,
        *,
        lock_path: Path,
        ttl_seconds: int = 600,
    ) -> None:
        self._lock_path = lock_path
        self._ttl_seconds = ttl_seconds

    @contextmanager
    def acquire(self) -> Iterator[AlarmImageRuntimeLock | None]:
        lock = self.try_acquire()

        try:
            yield lock
        finally:
            if lock is not None:
                self.release(lock)

    def try_acquire(self) -> AlarmImageRuntimeLock | None:
        self._lock_path.parent.mkdir(parents=True, exist_ok=True)

        owner = uuid4().hex
        now = datetime.now(UTC)
        expires_at = now + timedelta(seconds=self._ttl_seconds)

        payload = {
            'owner': owner,
            'created_at': now.isoformat(),
            'expires_at': expires_at.isoformat(),
        }

        try:
            self._create_lock_file(payload)
            return AlarmImageRuntimeLock(owner=owner)
        except FileExistsError:
            if self._is_expired():
                self._safe_unlink()
                try:
                    self._create_lock_file(payload)
                    return AlarmImageRuntimeLock(owner=owner)
                except FileExistsError:
                    return None

            return None

    def release(self, lock: AlarmImageRuntimeLock) -> None:
        try:
            data = json.loads(self._lock_path.read_text(encoding='utf-8'))
        except FileNotFoundError, json.JSONDecodeError, OSError:
            return

        if data.get('owner') != lock.owner:
            return

        self._safe_unlink()

    def _create_lock_file(self, payload: dict) -> None:
        flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY

        file_descriptor = os.open(self._lock_path, flags)

        with os.fdopen(file_descriptor, 'w', encoding='utf-8') as file:
            json.dump(payload, file, ensure_ascii=False)

    def _is_expired(self) -> bool:
        try:
            data = json.loads(self._lock_path.read_text(encoding='utf-8'))
        except FileNotFoundError, json.JSONDecodeError, OSError:
            return True

        expires_at_text = data.get('expires_at')

        if not expires_at_text:
            return True

        try:
            expires_at = datetime.fromisoformat(expires_at_text)
        except ValueError:
            return True

        return datetime.now(UTC) >= expires_at

    def _safe_unlink(self) -> None:
        try:
            self._lock_path.unlink()
        except FileNotFoundError:
            return
