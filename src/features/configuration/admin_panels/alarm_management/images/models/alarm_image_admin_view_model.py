from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4

PUBLISHED_STATUS = 'published'
REORDERED_STATUS = 'reordered'
DELETED_STATUS = 'deleted'
NEW_STATUS = 'new'
REPLACED_STATUS = 'replaced'


@dataclass(slots=True)
class AlarmImageAdminImage:
    message_group_key: str
    image_key: str
    order: int
    thumb_url: str
    full_url: str | None = None
    thumb_mime_type: str | None = None
    full_mime_type: str | None = None
    content_hash: str | None = None
    status: str = PUBLISHED_STATUS
    published_order: int | None = None
    source_filename: str | None = None
    draft_file_path: str | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> AlarmImageAdminImage:
        return cls(
            message_group_key=str(data['message_group_key']),
            image_key=str(data['image_key']),
            order=int(data['order']),
            thumb_url=str(data.get('thumb_url') or ''),
            full_url=data.get('full_url'),
            thumb_mime_type=data.get('thumb_mime_type'),
            full_mime_type=data.get('full_mime_type'),
            content_hash=data.get('content_hash'),
            status=str(data.get('status') or PUBLISHED_STATUS),
            published_order=data.get('published_order'),
            source_filename=data.get('source_filename'),
            draft_file_path=data.get('draft_file_path'),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            'message_group_key': self.message_group_key,
            'image_key': self.image_key,
            'order': self.order,
            'thumb_url': self.thumb_url,
            'full_url': self.full_url,
            'thumb_mime_type': self.thumb_mime_type,
            'full_mime_type': self.full_mime_type,
            'content_hash': self.content_hash,
            'status': self.status,
            'published_order': self.published_order,
            'source_filename': self.source_filename,
            'draft_file_path': self.draft_file_path,
        }


@dataclass(slots=True)
class AlarmImageAdminGroup:
    message_group_key: str
    label: str
    alarm_count: int = 0
    alarm_names: list[str] = field(default_factory=list)
    images: list[AlarmImageAdminImage] = field(default_factory=list)

    @property
    def active_images(self) -> list[AlarmImageAdminImage]:
        return sorted(
            [image for image in self.images if image.status != DELETED_STATUS],
            key=lambda image: image.order,
        )

    @property
    def image_count(self) -> int:
        return len(self.active_images)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> AlarmImageAdminGroup:
        return cls(
            message_group_key=str(data['message_group_key']),
            label=str(data.get('label') or data['message_group_key']),
            alarm_count=int(data.get('alarm_count') or 0),
            alarm_names=[str(value) for value in data.get('alarm_names', []) if str(value).strip()],
            images=[AlarmImageAdminImage.from_dict(image) for image in data.get('images', [])],
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            'message_group_key': self.message_group_key,
            'label': self.label,
            'alarm_count': self.alarm_count,
            'alarm_names': self.alarm_names,
            'image_count': self.image_count,
            'images': [
                image.to_dict() for image in sorted(self.images, key=lambda image: image.order)
            ],
        }


@dataclass(slots=True)
class AlarmImageChangeSummary:
    has_changes: bool = False
    only_order_changes: bool = False
    has_content_changes: bool = False
    changed_group_count: int = 0
    reordered_count: int = 0
    deleted_count: int = 0
    new_count: int = 0
    replaced_count: int = 0

    def to_dict(self) -> dict[str, Any]:
        return {
            'has_changes': self.has_changes,
            'only_order_changes': self.only_order_changes,
            'has_content_changes': self.has_content_changes,
            'changed_group_count': self.changed_group_count,
            'reordered_count': self.reordered_count,
            'deleted_count': self.deleted_count,
            'new_count': self.new_count,
            'replaced_count': self.replaced_count,
        }


@dataclass(slots=True)
class AlarmImageAdminDraft:
    groups: list[AlarmImageAdminGroup]
    draft_id: str = field(default_factory=lambda: uuid4().hex)
    selected_message_group_key: str | None = None
    search_text: str = ''
    current_page: int = 1
    page_size: int = 8
    ui_state: str = 'idle'
    error_message: str | None = None
    change_summary: AlarmImageChangeSummary = field(default_factory=AlarmImageChangeSummary)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> AlarmImageAdminDraft:
        return cls(
            groups=[AlarmImageAdminGroup.from_dict(group) for group in data.get('groups', [])],
            draft_id=str(data.get('draft_id') or uuid4().hex),
            selected_message_group_key=data.get('selected_message_group_key'),
            search_text=str(data.get('search_text') or ''),
            current_page=max(1, int(data.get('current_page') or 1)),
            page_size=max(1, int(data.get('page_size') or 8)),
            ui_state=str(data.get('ui_state') or 'idle'),
            error_message=data.get('error_message'),
            change_summary=AlarmImageChangeSummary(**data.get('change_summary', {})),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            'draft_id': self.draft_id,
            'groups': [group.to_dict() for group in self.groups],
            'selected_message_group_key': self.selected_message_group_key,
            'search_text': self.search_text,
            'current_page': self.current_page,
            'page_size': self.page_size,
            'ui_state': self.ui_state,
            'error_message': self.error_message,
            'change_summary': self.change_summary.to_dict(),
        }
