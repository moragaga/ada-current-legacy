from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class AlarmImageRuntimeItem:
    message_group_key: str
    image_key: str
    order: int
    label: str
    thumb_url: str
    full_url: str
    thumb_mime_type: str
    full_mime_type: str
    thumb_available: bool
    full_available: bool
    bundle_key: str
    bundle_hash: str
    content_hash: str | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> AlarmImageRuntimeItem:
        order = int(data.get('order') or 1)

        return cls(
            message_group_key=str(data.get('message_group_key') or '').strip(),
            image_key=str(data.get('image_key') or '').strip(),
            order=order,
            label=str(data.get('label') or f'Imagen {order}'),
            thumb_url=str(data.get('thumb_url') or '').strip(),
            full_url=str(data.get('full_url') or '').strip(),
            thumb_mime_type=str(data.get('thumb_mime_type') or '').strip(),
            full_mime_type=str(data.get('full_mime_type') or '').strip(),
            thumb_available=bool(data.get('thumb_available')),
            full_available=bool(data.get('full_available')),
            bundle_key=str(data.get('bundle_key') or '').strip(),
            bundle_hash=str(data.get('bundle_hash') or '').strip(),
            content_hash=data.get('content_hash'),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            'message_group_key': self.message_group_key,
            'image_key': self.image_key,
            'order': self.order,
            'label': self.label,
            'thumb_url': self.thumb_url,
            'full_url': self.full_url,
            'thumb_mime_type': self.thumb_mime_type,
            'full_mime_type': self.full_mime_type,
            'thumb_available': self.thumb_available,
            'full_available': self.full_available,
            'bundle_key': self.bundle_key,
            'bundle_hash': self.bundle_hash,
            'content_hash': self.content_hash,
        }


@dataclass(slots=True)
class AlarmImageRuntimeGroup:
    message_group_key: str
    images: list[AlarmImageRuntimeItem]
    has_images: bool
    has_missing_assets: bool

    def to_dict(self) -> dict[str, Any]:
        return {
            'message_group_key': self.message_group_key,
            'has_images': self.has_images,
            'has_missing_assets': self.has_missing_assets,
            'images': [image.to_dict() for image in self.images],
        }
