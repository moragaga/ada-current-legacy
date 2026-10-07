from __future__ import annotations

from src.features.configuration.models import Profile


class AuthorizationService:
    @staticmethod
    def can_access_admin(profile: str | None) -> bool:
        return profile in {
            Profile.ADMINISTRADOR.value,
            Profile.LOCAL.value,
        }

    @staticmethod
    def can_manage_alarms(profile: str | None) -> bool:
        return profile in {
            Profile.LOCAL.value,
            Profile.ADMINISTRADOR.value,
            Profile.GESTIONADOR.value,
        }

    @staticmethod
    def can_analyze(profile: str | None) -> bool:
        return profile in {
            Profile.LOCAL.value,
            Profile.ADMINISTRADOR.value,
            Profile.GESTIONADOR.value,
            Profile.ANALISTA.value,
        }

    @staticmethod
    def can_view(profile: str | None) -> bool:
        return profile in {
            Profile.LOCAL.value,
            Profile.ADMINISTRADOR.value,
            Profile.GESTIONADOR.value,
            Profile.ANALISTA.value,
            Profile.VISUALIZADOR.value,
        }
