from __future__ import annotations

from .file_type import SharepointFileType


class SharepointPathService:
    _TYPE_PATHS: dict[SharepointFileType, str] = {
        SharepointFileType.CONFIGURATION: 'configuration',
    }

    @classmethod
    def build_relative_path(
        cls, file_type: SharepointFileType, relative_path: str | None = None
    ) -> str:
        base_path = cls._TYPE_PATHS.get(
            file_type, cls._TYPE_PATHS[SharepointFileType.CONFIGURATION]
        )

        if not relative_path:
            return base_path

        normalized_relative = relative_path.strip('/\\')
        return f'{base_path}/{normalized_relative}'
