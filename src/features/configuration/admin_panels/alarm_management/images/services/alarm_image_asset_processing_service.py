from __future__ import annotations

import hashlib
import mimetypes
import shutil
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageOps


@dataclass(slots=True)
class ProcessedAlarmImageAsset:
    thumb_relative_path: str
    full_relative_path: str
    thumb_mime_type: str
    full_mime_type: str
    content_hash: str


class AlarmImageAssetProcessingService:
    def __init__(
        self,
        *,
        thumb_max_size: tuple[int, int] = (480, 480),
        thumb_quality: int = 90,
    ) -> None:
        self._thumb_max_size = thumb_max_size
        self._thumb_quality = thumb_quality

    def process_to_staging(
        self,
        *,
        source_path: Path,
        staging_bundle_dir: Path,
        message_group_key: str,
        image_key: str,
    ) -> ProcessedAlarmImageAsset:
        if not source_path.exists():
            raise FileNotFoundError(f'No existe la imagen fuente: {source_path}')

        full_extension = self._normalize_extension(source_path.suffix)
        full_mime_type = self._guess_mime_type(full_extension)

        full_relative_path = self._build_relative_path(
            variant='full',
            message_group_key=message_group_key,
            image_key=image_key,
            extension=full_extension,
        )
        thumb_relative_path = self._build_relative_path(
            variant='thumb',
            message_group_key=message_group_key,
            image_key=image_key,
            extension='.webp',
        )

        full_target_path = staging_bundle_dir / full_relative_path
        thumb_target_path = staging_bundle_dir / thumb_relative_path

        full_target_path.parent.mkdir(parents=True, exist_ok=True)
        thumb_target_path.parent.mkdir(parents=True, exist_ok=True)

        shutil.copyfile(source_path, full_target_path)
        self._create_thumb(
            source_path=source_path,
            target_path=thumb_target_path,
        )

        return ProcessedAlarmImageAsset(
            thumb_relative_path=thumb_relative_path.as_posix(),
            full_relative_path=full_relative_path.as_posix(),
            thumb_mime_type='image/webp',
            full_mime_type=full_mime_type,
            content_hash=self._sha256_file(full_target_path),
        )

    def _create_thumb(
        self,
        *,
        source_path: Path,
        target_path: Path,
    ) -> None:
        with Image.open(source_path) as image:
            image = ImageOps.exif_transpose(image)

            if image.mode not in {'RGB', 'RGBA'}:
                image = image.convert('RGB')

            image.thumbnail(self._thumb_max_size)

            target_path.parent.mkdir(parents=True, exist_ok=True)
            image.save(
                target_path,
                format='WEBP',
                quality=self._thumb_quality,
                method=4,
            )

    def _build_relative_path(
        self,
        *,
        variant: str,
        message_group_key: str,
        image_key: str,
        extension: str,
    ) -> Path:
        return (
            Path(variant)
            / self._safe_segment(message_group_key)
            / f'{self._safe_segment(image_key)}{extension}'
        )

    @staticmethod
    def _normalize_extension(extension: str) -> str:
        normalized_extension = extension.lower().strip()

        if normalized_extension == '.jpeg':
            return '.jpg'

        if normalized_extension in {'.jpg', '.png', '.webp'}:
            return normalized_extension

        raise ValueError(f'Extensión no permitida para imagen: {extension}')

    @staticmethod
    def _guess_mime_type(extension: str) -> str:
        mime_type, _ = mimetypes.guess_type(f'image{extension}')

        if mime_type:
            return mime_type

        if extension == '.jpg':
            return 'image/jpeg'

        if extension == '.png':
            return 'image/png'

        if extension == '.webp':
            return 'image/webp'

        return 'application/octet-stream'

    @staticmethod
    def _sha256_file(path: Path) -> str:
        digest = hashlib.sha256()

        with path.open('rb') as file:
            for chunk in iter(lambda: file.read(1024 * 1024), b''):
                digest.update(chunk)

        return digest.hexdigest()

    @staticmethod
    def _safe_segment(value: str) -> str:
        return (
            ''.join(
                char if char.isalnum() or char in {'_', '-'} else '_' for char in value.strip()
            ).strip('_')
            or 'unknown'
        )
