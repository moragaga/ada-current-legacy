from __future__ import annotations

import hashlib
import json
from typing import Any


class ConfigHashService:
    @staticmethod
    def build_hash(payload: Any) -> str:
        normalized_json = json.dumps(
            payload,
            ensure_ascii=False,
            sort_keys=True,
            separators=(',', ':'),
            default=str,
        )

        digest = hashlib.sha256(
            normalized_json.encode('utf-8'),
        ).hexdigest()

        return f'sha256:{digest}'
