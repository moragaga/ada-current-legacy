from __future__ import annotations

from datetime import datetime, timedelta, timezone

from src.features.alarm_management.domain import (
    SILENCE_POLICY_HOUR_CODES,
    SILENCE_POLICY_INHERIT,
    SILENCE_POLICY_NONE,
    SILENCE_POLICY_SHIFT_END,
    normalize_silence_policy_code,
)


class AlarmManagementPolicyService:
    MAX_SILENCE_HOURS = 11

    @classmethod
    def build_silence_options(
        cls,
        *,
        now_utc: datetime,
        shift_end_utc: datetime,
        max_hours: int | None = None,
    ) -> tuple[dict[str, str], ...]:
        now_utc = cls._ensure_aware_utc(now_utc)
        shift_end_utc = cls._ensure_aware_utc(shift_end_utc)

        remaining_seconds = int((shift_end_utc - now_utc).total_seconds())

        if remaining_seconds <= 0:
            return tuple()

        limit_hours = max(1, int(max_hours or cls.MAX_SILENCE_HOURS))

        full_hours = remaining_seconds // 3600
        remaining_minutes = (remaining_seconds % 3600) // 60
        has_partial_hour = remaining_minutes > 0 or remaining_seconds < 3600

        if full_hours >= limit_hours:
            return cls._build_hour_options(
                hours=limit_hours,
                has_partial_hour=has_partial_hour,
            )

        return cls._build_hour_options(
            hours=full_hours,
            has_partial_hour=has_partial_hour,
        )

    @classmethod
    def is_policy_available(
        cls,
        *,
        policy_code: str | None,
        now_utc: datetime,
        shift_end_utc: datetime,
    ) -> bool:
        normalized_policy = normalize_silence_policy_code(policy_code)

        available_values = {
            str(option.get('value') or '').strip()
            for option in cls.build_silence_options(
                now_utc=now_utc,
                shift_end_utc=shift_end_utc,
            )
        }

        return normalized_policy in available_values

    @staticmethod
    def resolve_effective_policy(
        *,
        policy_code: str | None,
        default_policy_code: str | None,
    ) -> str:
        normalized_policy = normalize_silence_policy_code(policy_code)
        normalized_default = normalize_silence_policy_code(default_policy_code)

        if normalized_policy == SILENCE_POLICY_INHERIT:
            normalized_policy = normalized_default

        if normalized_policy == SILENCE_POLICY_INHERIT:
            normalized_policy = SILENCE_POLICY_NONE

        AlarmManagementPolicyService._validate_policy_code(
            policy_code=normalized_policy,
        )

        return normalized_policy

    @staticmethod
    def calculate_silence_until(
        *,
        effective_policy_code: str,
        now_utc: datetime,
        shift_end_utc: datetime,
    ) -> datetime | None:
        policy_code = normalize_silence_policy_code(effective_policy_code)

        if policy_code == SILENCE_POLICY_NONE:
            return None

        now_utc = AlarmManagementPolicyService._ensure_aware_utc(now_utc)
        shift_end_utc = AlarmManagementPolicyService._ensure_aware_utc(shift_end_utc)

        if policy_code == SILENCE_POLICY_SHIFT_END:
            if shift_end_utc <= now_utc:
                raise ValueError(
                    'El fin de turno ya no está disponible. Vuelve a abrir la gestión.'
                )

            return shift_end_utc

        if policy_code in SILENCE_POLICY_HOUR_CODES:
            hours = int(policy_code.replace('h', ''))
            silence_until = now_utc + timedelta(hours=hours)

            if silence_until > shift_end_utc:
                raise ValueError(
                    'La duración seleccionada ya no está disponible. Selecciona una opción válida.'
                )

            return silence_until

        raise ValueError(f'Política de silencio inválida: {effective_policy_code}')

    @classmethod
    def _build_hour_options(
        cls,
        *,
        hours: list[int],
        has_partial_hour: bool,
    ) -> list[dict[str, str]]:
        options: list[dict[str, str]] = []

        for hour in range(1, hours + 1):
            options.append(cls._build_hour_option(hour=hour))

        if has_partial_hour:
            options.append(
                {
                    'label': 'Hasta fin de turno',
                    'value': SILENCE_POLICY_SHIFT_END,
                }
            )

        return tuple(options)

    @staticmethod
    def _build_hour_option(
        *,
        hour: int,
    ) -> dict[str, str]:
        return {
            'label': f'{hour} hora' if hour == 1 else f'{hour} horas',
            'value': f'h{hour:02d}',
        }

    @staticmethod
    def _validate_policy_code(
        *,
        policy_code: str,
    ) -> None:
        if policy_code == SILENCE_POLICY_NONE:
            return

        if policy_code == SILENCE_POLICY_SHIFT_END:
            return

        if policy_code in SILENCE_POLICY_HOUR_CODES:
            return

        raise ValueError(f'Política de silencio inválida: {policy_code}')

    @staticmethod
    def _ensure_aware_utc(value: datetime) -> datetime:
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)

        return value.astimezone(timezone.utc)
