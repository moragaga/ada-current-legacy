from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class AlarmImageBundleManifestRow:
    bundle_key: str
    bundle_hash: str
    bundle_filename: str
    bundle_relative_path: str
    size_bytes: int
    message_group_keys: list[str]
    updated_at: str
    published_at: str | None = None
    published_by: str | None = None
    published_by_email: str | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> AlarmImageBundleManifestRow:
        return cls(
            bundle_key=str(data.get('bundle_key') or '').strip(),
            bundle_hash=str(data.get('bundle_hash') or '').strip(),
            bundle_filename=str(data.get('bundle_filename') or '').strip(),
            bundle_relative_path=str(data.get('bundle_relative_path') or '').strip(),
            size_bytes=int(data.get('size_bytes') or 0),
            message_group_keys=_load_group_keys(data.get('message_group_keys_json')),
            updated_at=str(data.get('updated_at') or '').strip(),
            published_at=_clean_optional(data.get('published_at')),
            published_by=_clean_optional(data.get('published_by')),
            published_by_email=_clean_optional(data.get('published_by_email')),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            'bundle_key': self.bundle_key,
            'bundle_hash': self.bundle_hash,
            'bundle_filename': self.bundle_filename,
            'bundle_relative_path': self.bundle_relative_path,
            'size_bytes': self.size_bytes,
            'message_group_keys_json': json.dumps(
                self.message_group_keys,
                ensure_ascii=False,
                separators=(',', ':'),
            ),
            'updated_at': self.updated_at,
            'published_at': self.published_at or self.updated_at,
            'published_by': self.published_by or '',
            'published_by_email': self.published_by_email or '',
        }


def _load_group_keys(raw_value: Any) -> list[str]:
    if raw_value is None:
        return []

    if isinstance(raw_value, list):
        return [str(value).strip() for value in raw_value if str(value).strip()]

    text_value = str(raw_value).strip()

    if not text_value:
        return []

    try:
        parsed_value = json.loads(text_value)
    except json.JSONDecodeError:
        return [value.strip() for value in text_value.split(';') if value.strip()]

    if not isinstance(parsed_value, list):
        return []

    return [str(value).strip() for value in parsed_value if str(value).strip()]


def _clean_optional(value: Any) -> str | None:
    if value is None:
        return None

    text_value = str(value).strip()
    return text_value or None
