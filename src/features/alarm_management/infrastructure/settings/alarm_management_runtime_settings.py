from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AlarmManagementRuntimeSettings:
    runtime_snapshot_container_name: str = 'alarm_runtime_snapshot'
    runtime_snapshot_document_id: str = 'alarm_runtime_snapshot'
    runtime_snapshot_partition_key_value: str = 'alarm_runtime_snapshot'

    alarm_configuration_container_name: str = 'alarm_configuration'
    alarm_configuration_document_id: str = 'alarm_configuration'
    alarm_configuration_partition_key_value: str = 'alarm_configuration'

    message_configuration_container_name: str = 'alarm_management_message_configuration'
    message_configuration_document_id: str = 'alarm_management_message_configuration'
    message_configuration_partition_key_value: str = 'alarm_management_message_configuration'

    action_container_name: str = 'alarm_management_actions'
