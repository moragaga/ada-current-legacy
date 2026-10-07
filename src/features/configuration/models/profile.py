from __future__ import annotations

from enum import Enum


class Profile(str, Enum):
    ADMINISTRADOR = 'Administrador'
    VISUALIZADOR = 'Visualizador'
    GESTIONADOR = 'Gestionador'
    ANALISTA = 'Analista'
    LOCAL = 'Local'
    GUEST = 'Guest'

    @classmethod
    def values(cls) -> tuple[str, ...]:
        return tuple(member.value for member in cls)

    @classmethod
    def admin_values(cls) -> tuple[str, ...]:
        return cls.ADMINISTRADOR.value, cls.LOCAL.value

    @classmethod
    def assignable_values(cls) -> tuple[str, ...]:
        return (
            cls.ADMINISTRADOR.value,
            cls.GESTIONADOR.value,
            cls.ANALISTA.value,
            cls.VISUALIZADOR.value,
        )

    @classmethod
    def default_assignable(cls) -> str:
        return cls.VISUALIZADOR.value

    @classmethod
    def normalize_assignable(cls, value: str | None) -> str:
        normalized = str(value or '').strip()

        for profile in cls.assignable_values():
            if normalized.lower() == profile.lower():
                return profile

        return cls.default_assignable()
