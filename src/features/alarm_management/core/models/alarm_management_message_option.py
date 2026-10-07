from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from src.features.alarm_management.domain import (
    SILENCE_POLICY_INHERIT,
    normalize_silence_policy_code,
)


@dataclass(frozen=True)
class AlarmManagementMessageOption:
    message_id: str
    message: str
    sort_order: int = 0
    is_active: bool = True
    silence_policy_code: str = SILENCE_POLICY_INHERIT
    allow_silence_edit: bool = True
    source: str = 'global'

    @classmethod
    def from_dict(
        cls,
        *,
        data: dict[str, Any],
        source: str,
    ) -> 'AlarmManagementMessageOption | None':
        message_id = cls._text(data.get('message_id'))
        message = cls._text(data.get('message'))

        if not message_id or not message:
            return None

        return cls(
            message_id=message_id,
            message=message,
            sort_order=cls._int(data.get('sort_order'), default=0),
            is_active=cls._bool(data.get('is_active', True)),
            silence_policy_code=normalize_silence_policy_code(
                data.get('silence_policy_code') or data.get('default_silence_policy_code')
            ),
            allow_silence_edit=cls._bool(
                data.get('allow_silence_edit', True),
            ),
            source=source,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            'message_id': self.message_id,
            'message': self.message,
            'sort_order': self.sort_order,
            'is_active': self.is_active,
            'silence_policy_code': self.silence_policy_code,
            'allow_silence_edit': self.allow_silence_edit,
            'source': self.source,
        }

    def to_option(self) -> dict[str, str]:
        return {
            'label': self.message,
            'value': self.message_id,
        }

    @staticmethod
    def _text(value: Any) -> str:
        if value is None:
            return ''

        return str(value).strip()

    @staticmethod
    def _int(value: Any, *, default: int) -> int:
        if value is None or value == '':
            return default

        try:
            return int(float(value))
        except Exception:
            return default

    @staticmethod
    def _bool(value: Any) -> bool:
        if isinstance(value, bool):
            return value

        if value is None:
            return False

        if isinstance(value, str):
            return value.strip().lower() in {'true', '1', 'yes', 'si', 'sí'}

        return bool(value)
