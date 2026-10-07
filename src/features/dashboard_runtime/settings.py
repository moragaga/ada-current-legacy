from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DashboardRuntimeSettings:
    snapshot_container_name: str = 'kpi_runtime_snapshot'
    snapshot_document_id: str = 'kpi_runtime_snapshot'
    snapshot_partition_key: str = 'kpi_runtime_snapshot'

    @classmethod
    def from_env(cls) -> DashboardRuntimeSettings:
        return cls(
            snapshot_container_name=cls.snapshot_container_name,
            snapshot_document_id=cls.snapshot_document_id,
            snapshot_partition_key=cls.snapshot_partition_key,
        )


@dataclass(frozen=True)
class KpiConfigurationRuntimeSettings:
    kpi_configuration_container_name: str = 'kpi_configuration'
    kpi_configuration_document_id: str = 'kpi_configuration'

    @classmethod
    def from_env(cls) -> KpiConfigurationRuntimeSettings:
        return cls(
            kpi_configuration_container_name=cls.kpi_configuration_container_name,
            kpi_configuration_document_id=cls.kpi_configuration_document_id,
        )
