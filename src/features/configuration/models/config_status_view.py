from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ConfigArtifactStatusView:
    artifact_key: str
    display_name: str
    category: str
    sharepoint_revision: int
    sharepoint_hash: str
    sharepoint_updated_at: str
    sharepoint_updated_by: str | None
    published_revision: int | None
    published_hash: str | None
    published_at: str | None
    published_by: str | None
    status: str

    def to_row(self) -> dict:
        return {
            'artifact_key': self.artifact_key,
            'display_name': self.display_name,
            'category': self.category,
            'sharepoint_revision': self.sharepoint_revision,
            'sharepoint_updated_at': self.sharepoint_updated_at,
            'sharepoint_updated_by': self.sharepoint_updated_by,
            'published_revision': self.published_revision,
            'published_at': self.published_at,
            'published_by': self.published_by,
            'status': self._status_label(),
            'status_code': self.status,
        }

    def _status_label(self) -> str:
        if self.status == 'published':
            return 'Publicado'
        if self.status == 'pending_publish':
            return 'Pendiente'
        if self.status == 'unpublished':
            return 'No publicado'
        return self.status
