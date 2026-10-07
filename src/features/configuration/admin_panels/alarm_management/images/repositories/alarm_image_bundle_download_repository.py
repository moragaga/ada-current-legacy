from __future__ import annotations

from pathlib import PurePosixPath

from src.app.dependencies import get_configuration_sharepoint_repository


class AlarmImageBundleDownloadRepository:
    @staticmethod
    def download_bundle(
        *,
        bundle_relative_path: str,
    ) -> bytes:
        normalized_path = str(bundle_relative_path or '').strip().strip('/')

        if not normalized_path:
            raise ValueError('La ruta del bundle está vacía.')

        sharepoint_service = get_configuration_sharepoint_repository()

        path = PurePosixPath(normalized_path)
        filename = path.name
        relative_path = str(path.parent)

        content = sharepoint_service.download_file(
            filename=filename,
            relative_path=relative_path,
        )

        if not content:
            raise RuntimeError(
                f'No se pudo descargar el bundle desde SharePoint: {normalized_path}'
            )

        return content
