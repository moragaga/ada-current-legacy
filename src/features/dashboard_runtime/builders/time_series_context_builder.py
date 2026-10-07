from __future__ import annotations

from typing import Any

from src.shared.time.time_axis_builder import (
    build_local_time_axis,
    build_local_time_labels,
)

from ..models.kpi_configuration_definition import KpiConfigurationInformationDefinition


class TimeSeriesContextBuilder:
    def build(
        self,
        *,
        latest_time_series: dict | None,
        grouped_definitions: dict[str, list[KpiConfigurationInformationDefinition]],
    ) -> dict[str, Any]:
        latest_time_series: dict = latest_time_series or {}
        meta = latest_time_series.get('meta', {}) or {}
        sections = latest_time_series.get('sections', {}) or {}

        timestamps_payload = self._build_timestamps_payload(meta=meta)
        expected_length = meta.get('length', 0)

        result: dict[str, dict[str, list]] = {}

        for component, definitions in grouped_definitions.items():
            component_section = sections.get(component, {}) or {}
            configured_series = self._build_component_series(
                component_section=component_section,
                definitions=definitions,
                expected_length=expected_length,
            )
            result[component] = configured_series

        return {
            'time_series': result,
            'timestamps': timestamps_payload,
        }

    @staticmethod
    def _build_component_series(
        *,
        component_section: dict,
        definitions: list[KpiConfigurationInformationDefinition],
        expected_length: int,
    ) -> dict[str, list]:
        keys = component_section.get('keys', []) or []
        values = component_section.get('values', []) or []

        raw_series: dict[str, list] = {}
        for key, value in zip(keys, values, strict=False):
            if not isinstance(value, list):
                raw_series[key] = []
                continue

            if 0 < expected_length != len(value):
                raw_series[key] = []
                continue

            raw_series[key] = value

        result: dict[str, list] = {}
        for definition in definitions:
            if not definition.include_in_series_artifact:
                continue

            result[definition.kpi_name] = raw_series.get(definition.kpi_name, [])

        return result

    @staticmethod
    def _build_timestamps_payload(
        *,
        meta: dict | None,
    ) -> dict[str, Any]:
        meta: dict = meta or {}
        start_timestamp_utc = meta.get('start_timestamp')
        step_seconds = meta.get('step_seconds', 0)
        length = meta.get('length', 0)

        if not start_timestamp_utc or step_seconds <= 0 or length <= 0:
            return {
                'timestamps': [],
                'labels': [],
                'has_valid_data': False,
            }

        try:
            timestamps = build_local_time_axis(
                start_timestamp_utc=start_timestamp_utc,
                step_seconds=step_seconds,
                length=length,
            )
            labels = build_local_time_labels(axis_local=timestamps)
        except Exception as e:
            print(f'[ERROR] not build timestamps payload | exception={str(e)}')
            return {
                'timestamps': [],
                'labels': [],
                'has_valid_data': False,
            }

        return {
            'timestamps': timestamps,
            'labels': labels,
            'has_valid_data': True,
        }
