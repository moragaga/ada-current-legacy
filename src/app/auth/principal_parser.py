from __future__ import annotations

import base64
import json
import logging
from typing import Any

logger = logging.getLogger(__name__)


def parse_principal_header(principal_header: str | None) -> dict[str, Any] | None:
    if not principal_header:
        return None

    try:
        decoded = base64.b64decode(principal_header).decode('utf-8')
        return json.loads(decoded)
    except Exception as e:
        logger.exception(f'Failed to decode principal header {principal_header} - {e}')
        return None


def get_name_from_principal(principal_payload: dict | None, fallback_email: str) -> str:
    claims = (principal_payload or {}).get('claims', [])
    for claim in claims:
        if claim.get('typ') == 'name':
            return claim.get('val') or fallback_email.split('@')[0]
    return fallback_email.split('@')[0]
