from __future__ import annotations

from dataclasses import dataclass

from src.app.env_configuration import EnvConfiguration


@dataclass(frozen=True)
class SharepointSettings:
    get_endpoint: str = 'https://defaultd96f3d5a3042402a994b05725b2e14.27.environment.api.powerplatform.com:443/powerautomate/automations/direct/cu/03/workflows/7d5919866a144b56b70f61636731062b/triggers/manual/paths/invoke?api-version=1&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=_uaA9NRpQXOY9g5Si7iGaG4TIYejHQxh01PHtIGEmP4'
    post_endpoint: str = 'https://defaultd96f3d5a3042402a994b05725b2e14.27.environment.api.powerplatform.com:443/powerautomate/automations/direct/cu/00/workflows/b8f1cbae44bc41569ff6851ffc6fd83d/triggers/manual/paths/invoke?api-version=1&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=dw5BQ3qeP9ADJt3Rr_ktv6qRQ4hK3wSiAcYBpPiF8Xs'
    root_path: str = ''
    headers: dict | None = None

    @classmethod
    def from_env(cls, settings: EnvConfiguration) -> SharepointSettings:
        return cls(
            get_endpoint=cls.get_endpoint,
            post_endpoint=cls.post_endpoint,
            root_path=settings.sharepoint_root_path,
            headers={'app-access-token': settings.secret_key},
        )
