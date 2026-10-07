from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AlarmRuntimeSettings:
    alarm_container_name: str = 'alarm_runtime_snapshot'
    alarm_document_id: str = 'alarm_runtime_snapshot'

    @classmethod
    def from_env(cls) -> AlarmRuntimeSettings:
        return cls(
            alarm_container_name=cls.alarm_container_name,
            alarm_document_id=cls.alarm_document_id,
        )
