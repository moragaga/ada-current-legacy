from __future__ import annotations

from typing import Any

from src.features.alarm_management.domain import SILENCE_POLICY_CODES


class AlarmMessageRowValidator:
    @staticmethod
    def normalize_and_validate_rows(
        *,
        rows: list[dict[str, Any]] | None,
    ) -> list[dict[str, Any]]:
        normalized_rows: list[dict[str, Any]] = []
        seen_codes: set[str] = set()

        for raw_row in rows or []:
            if not isinstance(raw_row, dict):
                continue

            if AlarmMessageRowValidator._is_empty_row(raw_row):
                continue

            message_id = str(raw_row.get('message_id') or '').strip()
            message = str(raw_row.get('message') or '').strip()
            silence_policy_code = str(raw_row.get('silence_policy_code') or '').strip()

            if not message_id:
                raise ValueError('Existe una fila sin código de mensaje.')

            if not message:
                raise ValueError(f'El mensaje "{message_id}" no tiene texto.')

            if message_id in seen_codes:
                raise ValueError(
                    f'El código de mensaje "{message_id}" está duplicado '
                    'dentro del grupo seleccionado.'
                )

            if silence_policy_code not in SILENCE_POLICY_CODES:
                raise ValueError(
                    f'La política de silencio "{silence_policy_code}" '
                    f'del mensaje "{message_id}" no es válida.'
                )

            seen_codes.add(message_id)

            normalized_rows.append(
                {
                    'message_id': message_id,
                    'message': message,
                    'silence_policy_code': silence_policy_code,
                    'allow_silence_edit': AlarmMessageRowValidator._to_bool(
                        raw_row.get('allow_silence_edit'),
                        default=True,
                    ),
                    'is_active': AlarmMessageRowValidator._to_bool(
                        raw_row.get('is_active'),
                        default=True,
                    ),
                    'sort_order': AlarmMessageRowValidator._to_int(
                        raw_row.get('sort_order'),
                        default=0,
                    ),
                }
            )

        return sorted(
            normalized_rows,
            key=lambda item: (
                int(item.get('sort_order') or 0),
                str(item.get('message') or ''),
            ),
        )

    @staticmethod
    def _is_empty_row(row: dict[str, Any]) -> bool:
        message_id = str(row.get('message_id') or '').strip()
        message = str(row.get('message') or '').strip()

        return not message_id and not message

    @staticmethod
    def _to_bool(value: Any, *, default: bool) -> bool:
        if value is None:
            return default

        if isinstance(value, bool):
            return value

        if isinstance(value, str):
            return value.strip().lower() in {
                'true',
                '1',
                'yes',
                'y',
                'si',
                'sí',
            }

        return bool(value)

    @staticmethod
    def _to_int(value: Any, *, default: int) -> int:
        if value is None or value == '':
            return default

        return int(value)
