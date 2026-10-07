from __future__ import annotations

import hashlib
import os
import shutil
import zipfile
from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class AlarmImageBundleZip:
    bundle_key: str
    bundle_hash: str
    filename: str
    path: Path
    size_bytes: int


class AlarmImagePublicAssetRepository:
    def __init__(
        self,
        *,
        public_assets_root: Path | None = None,
        staging_root: Path | None = None,
        bundle_zip_root: Path | None = None,
    ) -> None:
        self._public_assets_root = public_assets_root or Path(
            os.getenv(
                'MANAGED_ALARM_IMAGE_PUBLIC_ASSETS_ROOT',
                'src/assets/data/managed_alarm_images/public',
            )
        )
        self._staging_root = staging_root or Path(
            os.getenv(
                'MANAGED_ALARM_IMAGE_STAGING_ROOT',
                'runtime_cache/managed_alarm_images/staging',
            )
        )
        self._bundle_zip_root = bundle_zip_root or Path(
            os.getenv(
                'MANAGED_ALARM_IMAGE_BUNDLE_ROOT',
                'runtime_cache/managed_alarm_images/bundles',
            )
        )

    def prepare_staging_dir(
        self,
        *,
        bundle_key: str,
        trace_id: str,
    ) -> Path:
        staging_dir = (
            self._staging_root / self._safe_segment(bundle_key) / self._safe_segment(trace_id)
        )

        if staging_dir.exists():
            shutil.rmtree(staging_dir)

        staging_dir.mkdir(parents=True, exist_ok=True)
        return staging_dir

    def commit_bundle(
        self,
        *,
        bundle_key: str,
        bundle_hash: str,
        staging_dir: Path,
    ) -> Path:
        final_dir = self.get_bundle_public_dir(
            bundle_key=bundle_key,
            bundle_hash=bundle_hash,
        )

        if final_dir.exists():
            shutil.rmtree(final_dir)

        final_dir.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(staging_dir, final_dir)

        return final_dir

    def get_bundle_public_dir(
        self,
        *,
        bundle_key: str,
        bundle_hash: str,
    ) -> Path:
        return (
            self._public_assets_root
            / self._safe_segment(bundle_key)
            / self._safe_segment(bundle_hash)
        )

    def has_public_bundle(
        self,
        *,
        bundle_key: str,
        bundle_hash: str,
    ) -> bool:
        bundle_dir = self.get_bundle_public_dir(
            bundle_key=bundle_key,
            bundle_hash=bundle_hash,
        )
        return bundle_dir.exists() and bundle_dir.is_dir()

    def create_bundle_zip(
        self,
        *,
        bundle_key: str,
        bundle_hash: str,
        bundle_dir: Path,
    ) -> AlarmImageBundleZip:
        self._bundle_zip_root.mkdir(parents=True, exist_ok=True)

        filename = f'{self._safe_segment(bundle_key)}__{self._safe_segment(bundle_hash)}.zip'
        zip_path = self._bundle_zip_root / filename

        if zip_path.exists():
            zip_path.unlink()

        with zipfile.ZipFile(zip_path, mode='w', compression=zipfile.ZIP_STORED) as zip_file:
            for file_path in sorted(bundle_dir.rglob('*')):
                if not file_path.is_file():
                    continue

                zip_file.write(
                    file_path,
                    arcname=file_path.relative_to(bundle_dir).as_posix(),
                )

        return AlarmImageBundleZip(
            bundle_key=bundle_key,
            bundle_hash=bundle_hash,
            filename=filename,
            path=zip_path,
            size_bytes=zip_path.stat().st_size,
        )

    @staticmethod
    def compute_directory_hash(directory: Path) -> str:
        digest = hashlib.sha256()

        for file_path in sorted(directory.rglob('*')):
            if not file_path.is_file():
                continue

            relative_path = file_path.relative_to(directory).as_posix()
            digest.update(relative_path.encode('utf-8'))
            digest.update(b'\0')

            with file_path.open('rb') as file:
                for chunk in iter(lambda: file.read(1024 * 1024), b''):
                    digest.update(chunk)

            digest.update(b'\0')

        return digest.hexdigest()

    def build_public_path(
        self,
        *,
        bundle_key: str,
        bundle_hash: str,
        relative_path: str,
    ) -> str:
        return (
            f'{self._safe_segment(bundle_key)}/'
            f'{self._safe_segment(bundle_hash)}/'
            f'{relative_path.strip("/")}'
        )

    def resolve_public_asset_path(self, path: str) -> Path:
        normalized_path = self._strip_public_prefix(path)
        return self._public_assets_root / normalized_path

    @staticmethod
    def cleanup_staging_dir(staging_dir: Path) -> None:
        if staging_dir.exists():
            shutil.rmtree(staging_dir)

    @staticmethod
    def _strip_public_prefix(value: str) -> Path:
        raw_value = str(value or '').strip().strip('/')

        prefixes = (
            'assets/data/managed_alarm_images/public/',
            '/assets/data/managed_alarm_images/public/',
        )

        for prefix in prefixes:
            normalized_prefix = prefix.strip('/')
            if raw_value.startswith(normalized_prefix):
                raw_value = raw_value[len(normalized_prefix) :].strip('/')
                break

        return Path(raw_value)

    @staticmethod
    def _safe_segment(value: str) -> str:
        return (
            ''.join(
                char if char.isalnum() or char in {'_', '-'} else '_' for char in value.strip()
            ).strip('_')
            or 'unknown'
        )
