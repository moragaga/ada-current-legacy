from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

_INTEGRATED_OPERATIONS_COMPONENTS = (
    'general',
    'time',
    'indicadores_globales',
    'general_mina',
    'carguio',
    'transporte',
    'carguio_transporte',
    'chancado_stmg',
    'stock_chacay',
    'molienda',
    'flotacion',
    'transporte_fluidos',
    'puerto',
)

_PROCESS_COMPONENTS = (
    'general',
    'time',
    'indicadores_globales',
    'center',
    'left',
    'right',
    'bottom',
)

_STRATEGIC_COMPONENTS = ('general', 'time', 'indicadores_globales',)


class AppRuntimeProfile(str, Enum):
    INTEGRATED_OPERATIONS = 'IO'
    PROCESS = 'PRO'
    STRATEGIC = 'STR'

    def build_components(self) -> tuple[str, ...]:
        if self == AppRuntimeProfile.INTEGRATED_OPERATIONS:
            return _INTEGRATED_OPERATIONS_COMPONENTS

        if self == AppRuntimeProfile.PROCESS:
            return _PROCESS_COMPONENTS

        if self == AppRuntimeProfile.STRATEGIC:
            return _STRATEGIC_COMPONENTS

        raise ValueError(f'[ERROR] Invalid app runtime profile: {self}')


@dataclass(frozen=True, slots=True)
class AppRuntimeProfileData:
    components: tuple[str, ...] = field(default_factory=tuple)
    default_component: str = 'indicadores_globales'
    include_timelines: bool = True
    include_timestamps: bool = True


@dataclass(frozen=True, slots=True)
class AppRuntimeProfileSettings:
    profile: AppRuntimeProfile
    data: AppRuntimeProfileData

    @classmethod
    def from_value(cls, value: str | None) -> AppRuntimeProfileSettings:
        if value is None or not value.strip():
            raise ValueError('[ERROR] APP_RUNTIME_PROFILE is required')

        profile = AppRuntimeProfile(value)

        return cls(
            profile=profile,
            data=AppRuntimeProfileData(
                components=profile.build_components(),
            ),
        )

    @property
    def profile_value(self) -> AppRuntimeProfile:
        return self.profile
