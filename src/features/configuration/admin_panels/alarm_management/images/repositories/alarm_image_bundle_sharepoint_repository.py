from __future__ import annotations

from pathlib import Path

from src.app.dependencies import get_configuration_sharepoint_repository


class AlarmImageBundleSharePointRepository:
    def __init__(
        self,
        *,
        relative_path: str = 'alarm/image_bundles',
    ) -> None:
        self._relative_path = relative_path.strip('/')

    def upload_bundle_zip(
        self,
        *,
        zip_path: Path,
        bundle_filename: str,
    ) -> str:
        if not zip_path.exists():
            raise FileNotFoundError(f'No existe el ZIP del bundle: {zip_path}')

        content = zip_path.read_bytes()
        sharepoint_service = get_configuration_sharepoint_repository()

        saved = sharepoint_service.upload_file(
            relative_path=self._relative_path,
            filename=bundle_filename,
            content=content,
        )

        if not saved:
            raise RuntimeError(f'No se pudo subir el bundle ZIP a SharePoint: {bundle_filename}')

        return f'{self._relative_path}/{bundle_filename}'
