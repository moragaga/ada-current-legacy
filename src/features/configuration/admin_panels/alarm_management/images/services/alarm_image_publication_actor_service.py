from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from src.app.auth.identity_context import get_current_profile


@dataclass(slots=True)
class AlarmImagePublicationActor:
    display_name: str
    email: str


class AlarmImagePublicationActorService:
    def get_current_actor(self) -> AlarmImagePublicationActor:
        try:
            profile = get_current_profile()
        except Exception:
            profile = None

        display_name = self._get_first_value(
            profile,
            keys=[
                'display_name',
                'name',
                'full_name',
                'user_name',
            ],
        )
        email = self._get_first_value(
            profile,
            keys=[
                'email',
                'mail',
                'user_email',
                'preferred_username',
            ],
        )

        if not display_name and email:
            display_name = email

        return AlarmImagePublicationActor(
            display_name=display_name or 'Sistema',
            email=email or '',
        )

    def _get_first_value(
        self,
        source: Any,
        *,
        keys: list[str],
    ) -> str:
        if source is None:
            return ''

        for key in keys:
            value = self._get_value(source, key)

            if value:
                return value

        return ''

    @staticmethod
    def _get_value(
        source: Any,
        key: str,
    ) -> str:
        if isinstance(source, dict):
            value = source.get(key)
        else:
            value = getattr(source, key, None)

        if value is None:
            return ''

        return str(value).strip()
