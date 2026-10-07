from __future__ import annotations

from src.features.admin_framework.services import build_admin_layout

from .definition import IDENTITY_USERS_ADMIN_DEFINITION


def build_identity_users_admin_layout():
    return build_admin_layout(IDENTITY_USERS_ADMIN_DEFINITION)
