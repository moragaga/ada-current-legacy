from __future__ import annotations

from typing import Any
from uuid import uuid4

from src.features.configuration.models import Profile


class IdentityUserRowFactoryService:
    @staticmethod
    def build_new_row() -> dict[str, Any]:
        return {
            'user_id': str(uuid4()),
            'name': '',
            'email': '',
            'profile': Profile.default_assignable(),
            'is_active': True,
        }
