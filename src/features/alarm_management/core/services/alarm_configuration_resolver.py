from __future__ import annotations

from typing import Any


class AlarmConfigurationResolver:
    @staticmethod
    def find_by_alarm_key(
        *,
        alarm_configuration_rows: list[dict[str, Any]],
        alarm_key: str,
    ) -> dict[str, Any] | None:
        target_alarm_key = str(alarm_key or '').strip()

        if not target_alarm_key:
            return None

        for row in alarm_configuration_rows:
            if not isinstance(row, dict):
                continue

            current_alarm_key = str(row.get('alarm_key') or '').strip()

            if current_alarm_key == target_alarm_key:
                return row

        return None

    @staticmethod
    def build_by_alarm_key(
        *,
        alarm_configuration_rows: list[dict[str, Any]],
    ) -> dict[str, dict[str, Any]]:
        result: dict[str, dict[str, Any]] = {}

        for row in alarm_configuration_rows:
            if not isinstance(row, dict):
                continue

            alarm_key = str(row.get('alarm_key') or '').strip()

            if not alarm_key:
                continue

            result[alarm_key] = row

        return result
