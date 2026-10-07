from __future__ import annotations

import json
import math

from ..models.kpi_configuration_definition import KpiConfigurationInformationDefinition


class InstantItemsMapper:
    def build(
        self,
        *,
        latest_instant: dict | None,
        grouped_definitions: dict[str, list[KpiConfigurationInformationDefinition]],
    ) -> dict[str, dict[str, dict]]:
        latest_instant = latest_instant or {}
        result: dict[str, dict[str, dict]] = {}

        for component, definitions in grouped_definitions.items():
            component_latest = latest_instant.get(component, {})
            result[component] = {}

            for definition in definitions:
                if not definition.load_instant:
                    continue

                result[component][definition.kpi_name] = self._resolve_value_payload(
                    definition=definition,
                    latest_instant=component_latest,
                )

            # Valor default para no mapeado
            result[component][''] = {
                'value': None,
                'status': 'missing',
            }

        return result

    def _resolve_value_payload(
        self,
        *,
        definition: KpiConfigurationInformationDefinition,
        latest_instant: dict | None,
    ) -> dict[str, object]:
        if not isinstance(latest_instant, dict):
            return {'value': None, 'status': 'missing'}

        if definition.kpi_name not in latest_instant:
            return {'value': None, 'status': 'missing'}

        value = latest_instant.get(definition.kpi_name)

        if self._is_invalid_value(value):
            return {'value': None, 'status': 'invalid'}

        if definition.visualization == 'json':
            return self._extract_json_value(value)

        return {'value': value, 'status': 'ok'}

    @staticmethod
    def _is_invalid_value(value: object) -> bool:
        if value is None:
            return True

        if isinstance(value, str) and value.strip().lower() == 'nan':
            return True

        if isinstance(value, float) and math.isnan(value):
            return True

        return False

    @staticmethod
    def _extract_json_value(value: str) -> dict[str, object]:
        try:
            return {
                'value': json.loads(value),
                'status': 'ok',
            }
        except TypeError, json.JSONDecodeError:
            return {
                'value': None,
                'status': 'invalid',
            }
