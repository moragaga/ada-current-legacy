from __future__ import annotations

import traceback
from typing import Any

from dash.development.base_component import Component

from src.shared.ui.display.error_component import build_error_component
from src.shared.ui.rendering.kpis.models import KpiBuildDefinition


def build_content(
    *,
    definition: list[KpiBuildDefinition],
    kpis: dict | None = None,
    timeseries: dict | None = None,
    timestamps: dict | None = None,
) -> list[Component]:
    builder_kwargs: dict[str, Any] = {}
    if kpis is not None:
        builder_kwargs['kpis'] = kpis
    if timeseries is not None:
        builder_kwargs['timeseries'] = timeseries
    if timestamps is not None:
        builder_kwargs['timestamps'] = timestamps

    return _build_components_safely(definitions=definition, **builder_kwargs)


def _build_component_safely(
    *,
    definition: KpiBuildDefinition,
    **builder_kwargs,
) -> Component:
    try:
        return definition.builder(**builder_kwargs)
    except Exception as e:
        print(f'[ERROR] slot={definition.slot_name} error={e}')
        traceback.print_exc()
        return build_error_component(ui_size=definition.ui_size)


def _build_components_safely(
    *,
    definitions: list[KpiBuildDefinition],
    **builder_kwargs,
) -> list[Component]:
    components: list[Component] = []
    for definition in definitions:
        builder_kwargs_tmp = _exclude_parameters(
            exclude_parameters=definition.exclude_parameters, builder_kwargs=builder_kwargs
        )

        component = _build_component_safely(definition=definition, **builder_kwargs_tmp)
        if definition.explicit_list:
            components.extend(component)
            continue
        components.append(component)
    return components


def _exclude_parameters(
    exclude_parameters: list[str],
    builder_kwargs: dict,
):
    builder_kwargs_tmp = dict(builder_kwargs).copy()
    if exclude_parameters is not None:
        for parameter in exclude_parameters:
            builder_kwargs_tmp.pop(parameter, None)
    return builder_kwargs_tmp
