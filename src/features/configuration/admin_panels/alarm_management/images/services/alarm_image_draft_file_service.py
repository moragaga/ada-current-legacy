from __future__ import annotations

import base64
import hashlib
import os
import re
from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class SavedDraftImage:
    image_key: str
    source_filename: str
    mime_type: str
    content_hash: str
    asset_url: str
    file_path: str


class AlarmImageDraftFileService:
    _ALLOWED_MIME_TYPES = {
        'image/jpeg': '.jpg',
        'image/png': '.png',
    }

    def __init__(
        self,
        *,
        draft_assets_root: Path | None = None,
        draft_asset_url_prefix: str | None = None,
        max_size_bytes: int = 5 * 1024 * 1024,
    ) -> None:
        self._draft_assets_root = draft_assets_root or Path(
            os.getenv(
                'MANAGED_ALARM_IMAGE_DRAFT_ASSETS_ROOT',
                'src/assets/data/managed_alarm_images/draft',
            )
        )

        self._draft_asset_url_prefix = (
            draft_asset_url_prefix
            or os.getenv(
                'MANAGED_ALARM_IMAGE_DRAFT_ASSET_URL_PREFIX',
                '/assets/data/managed_alarm_images/draft',
            )
        ).rstrip('/')

        self._max_size_bytes = max_size_bytes

    def save_uploaded_image(
        self,
        *,
        contents: str,
        filename: str,
        draft_id: str,
        message_group_key: str,
        image_key: str,
    ) -> SavedDraftImage:
        mime_type, binary = self._decode_upload(contents)

        if mime_type not in self._ALLOWED_MIME_TYPES:
            raise ValueError('Formato no permitido. Usa JPG, JPEG o PNG.')

        if len(binary) > self._max_size_bytes:
            raise ValueError('La imagen supera el tamaño máximo permitido.')

        extension = self._ALLOWED_MIME_TYPES[mime_type]
        content_hash = hashlib.sha256(binary).hexdigest()

        safe_group_key = self._safe_path_segment(message_group_key)
        safe_draft_id = self._safe_path_segment(draft_id)
        safe_image_key = self._safe_path_segment(image_key)

        target_dir = self._draft_assets_root / safe_draft_id / safe_group_key / safe_image_key
        target_dir.mkdir(parents=True, exist_ok=True)

        target_path = target_dir / f'original{extension}'
        target_path.write_bytes(binary)

        asset_url = (
            f'{self._draft_asset_url_prefix}/'
            f'{safe_draft_id}/'
            f'{safe_group_key}/'
            f'{safe_image_key}/'
            f'original{extension}'
        )

        return SavedDraftImage(
            image_key=image_key,
            source_filename=filename,
            mime_type=mime_type,
            content_hash=content_hash,
            asset_url=asset_url,
            file_path=str(target_path),
        )

    @staticmethod
    def _decode_upload(contents: str) -> tuple[str, bytes]:
        if not contents or ',' not in contents:
            raise ValueError('No se recibió una imagen válida.')

        header, payload = contents.split(',', 1)

        mime_type_match = re.match(r'^data:(?P<mime>[-\w.]+/[-\w+.]+);base64$', header)
        if not mime_type_match:
            raise ValueError('Formato de carga inválido.')

        mime_type = mime_type_match.group('mime')
        binary = base64.b64decode(payload, validate=True)

        return mime_type, binary

    @staticmethod
    def _safe_path_segment(value: str) -> str:
        safe_value = re.sub(r'[^a-zA-Z0-9_-]+', '_', value.strip())
        safe_value = safe_value.strip('_')
        return safe_value or 'unknown'
