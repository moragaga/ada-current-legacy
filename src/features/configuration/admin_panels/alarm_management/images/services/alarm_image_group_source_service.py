from __future__ import annotations

from collections import defaultdict
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

AlarmConfigurationRowsLoader = Callable[[], list[dict[str, Any]]]


@dataclass(slots=True)
class AlarmImageMessageGroup:
    message_group_key: str
    label: str
    alarm_count: int
    alarm_names: list[str]

    def to_dict(self) -> dict[str, Any]:
        return {
            'message_group_key': self.message_group_key,
            'label': self.label,
            'alarm_count': self.alarm_count,
            'alarm_names': self.alarm_names,
        }


class AlarmImageGroupSourceService:
    def __init__(
        self,
        *,
        load_alarm_configuration_rows: AlarmConfigurationRowsLoader,
    ) -> None:
        self._load_alarm_configuration_rows = load_alarm_configuration_rows

    def load_message_groups(self) -> list[dict[str, Any]]:
        rows = self._load_alarm_configuration_rows()
        groups = self._build_groups(rows)

        return [
            group.to_dict()
            for group in sorted(groups, key=lambda item: item.message_group_key.lower())
        ]

    def _build_groups(
        self,
        rows: list[dict[str, Any]],
    ) -> list[AlarmImageMessageGroup]:
        rows_by_group_key: dict[str, list[dict[str, Any]]] = defaultdict(list)

        for row in rows:
            message_group_key = self._get_message_group_key(row)

            if not message_group_key:
                continue

            rows_by_group_key[message_group_key].append(row)

        return [
            AlarmImageMessageGroup(
                message_group_key=message_group_key,
                label=message_group_key,
                alarm_count=len(group_rows),
                alarm_names=self._build_alarm_names(group_rows),
            )
            for message_group_key, group_rows in rows_by_group_key.items()
        ]

    @staticmethod
    def _get_message_group_key(row: dict[str, Any]) -> str:
        value = row.get('message_group_key')

        if value is None:
            return ''

        return str(value).strip()

    def _build_alarm_names(self, rows: list[dict[str, Any]]) -> list[str]:
        names = []

        for row in rows:
            name = self._get_alarm_name(row)

            if name and name not in names:
                names.append(name)

        return sorted(names, key=str.lower)

    @staticmethod
    def _get_alarm_name(row: dict[str, Any]) -> str:
        for key in ('alarm_display_name', 'title', 'alarm_key'):
            value = row.get(key)

            if value is None:
                continue

            normalized_value = str(value).strip()

            if normalized_value:
                return normalized_value

        return ''
