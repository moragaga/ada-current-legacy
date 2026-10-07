from __future__ import annotations

from flask import session

from src.features.navigation.models import (
    NavigationRuntimeConfig,
)

from ..dependencies import get_navigation_cache_service


def load_request_navigation(
    force_refresh: bool = False,
) -> NavigationRuntimeConfig:
    config = get_navigation_cache_service().get_navigation(
        force_refresh=force_refresh,
    )

    session['navigation_runtime_config'] = config.to_dict()
    session.modified = True

    return config
