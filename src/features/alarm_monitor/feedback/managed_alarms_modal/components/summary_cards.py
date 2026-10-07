from __future__ import annotations

from typing import Any

import dash_bootstrap_components as dbc
from dash import html

from ..constants import (
    DEFAULT_TURN_SCOPE_FILTER,
    TURN_SCOPE_ALL,
)
from .states import build_initial_summary_state


def build_summary_cards(
    *,
    snapshot: dict[str, Any] | None,
    turn_scope_filter: str | None = None,
) -> list[Any]:
    if not snapshot:
        return [build_initial_summary_state()]

    summary = _select_summary_metrics(
        snapshot=snapshot,
        turn_scope_filter=turn_scope_filter,
    )

    return [
        _build_summary_card(
            label='Gestiones',
            value=_metric_value(
                summary,
                'management_count',
                'total_managements',
            ),
            icon_class_name='bi bi-check2-circle',
            hint='Gestiones efectivas.',
        ),
        _build_summary_card(
            label='Manuales',
            value=_metric_value(
                summary,
                'manual_management_count',
                'manual_managements',
            ),
            icon_class_name='bi bi-person-check',
            hint='Gestiones normales.',
        ),
        _build_summary_card(
            label='Desactivadas',
            value=_metric_value(
                summary,
                'inactive_management_count',
                'inactive_managements',
            ),
            icon_class_name='bi bi-pause-circle',
            hint='Bloqueo por inactividad.',
        ),
        _build_summary_card(
            label='Tiempo medio',
            value=_duration_value(
                summary=summary,
                # label_key='average_time_to_management_label',
                seconds_key='average_time_to_management_seconds',
            ),
            icon_class_name='bi bi-stopwatch',
            hint='Promedio hasta gestión.',
        ),
        # _build_summary_card(
        #     label='Alarmas distintas',
        #     value=_metric_value(
        #         summary,
        #         'unique_alarm_count',
        #     ),
        #     icon_class_name='bi bi-bell',
        #     hint='Alarmas únicas gestionadas.',
        # ),
        # _build_summary_card(
        #     label='Ocurrencias',
        #     value=_metric_value(
        #         summary,
        #         'unique_occurrence_count',
        #     ),
        #     icon_class_name='bi bi-diagram-3',
        #     hint='Ocurrencias gestionadas.',
        # ),
        _build_summary_card(
            label='Siguen activas',
            value=_metric_value(
                summary,
                'managed_still_active_count',
            ),
            icon_class_name='bi bi-activity',
            hint='Gestionadas aún activas.',
        ),
        _build_summary_card(
            label='Inactividades',
            value=_metric_value(
                summary,
                'active_inactivity_count',
            ),
            icon_class_name='bi bi-hourglass-split',
            hint='Bloqueos vigentes.',
        ),
        # _build_summary_card(
        #     label='Tiempo mediano',
        #     value=_duration_value(
        #         summary=summary,
        #         label_key='median_time_to_management_label',
        #         seconds_key='median_time_to_management_seconds',
        #     ),
        #     icon_class_name='bi bi-clock-history',
        #     hint='Mediana hasta gestión.',
        # ),
        # _build_summary_card(
        #     label='Tiempo máximo',
        #     value=_duration_value(
        #         summary=summary,
        #         label_key='max_time_to_management_label',
        #         seconds_key='max_time_to_management_seconds',
        #     ),
        #     icon_class_name='bi bi-alarm',
        #     hint='Mayor tiempo hasta gestión.',
        # ),
    ]


def _select_summary_metrics(
    *,
    snapshot: dict[str, Any],
    turn_scope_filter: str | None,
) -> dict[str, Any]:
    summary = _as_dict(snapshot.get('summary_metrics'))

    selected_scope = (
        _safe_str(turn_scope_filter)
        or _safe_str(snapshot.get('default_turn_scope_filter'))
        or DEFAULT_TURN_SCOPE_FILTER
    )

    if selected_scope == TURN_SCOPE_ALL:
        return summary

    by_turn_scope = _as_dict(summary.get('by_turn_scope'))

    if by_turn_scope:
        return _as_dict(by_turn_scope.get(selected_scope))

    return summary


def _build_summary_card(
    *,
    label: str,
    value: str,
    icon_class_name: str,
    hint: str,
) -> dbc.Card:
    return dbc.Card(
        className='managed-alarms-summary-card',
        children=[
            html.Div(
                className='managed-alarms-summary-icon',
                children=[
                    html.I(className=icon_class_name),
                ],
            ),
            html.Div(
                className='managed-alarms-summary-content',
                children=[
                    html.Div(
                        value,
                        className='managed-alarms-summary-value',
                    ),
                    html.Div(
                        label,
                        className='managed-alarms-summary-label',
                    ),
                    html.Div(
                        hint,
                        className='managed-alarms-summary-hint',
                    ),
                ],
            ),
        ],
    )


def _metric_value(
    summary: dict[str, Any],
    *keys: str,
    default: Any = 0,
) -> str:
    for key in keys:
        if key not in summary:
            continue

        value = summary.get(key)

        if value is None or value == '':
            continue

        return _safe_str(value)

    return _safe_str(default)


def _duration_value(
    *,
    summary: dict[str, Any],
    # label_key: str,
    seconds_key: str,
) -> str:
    # label = _safe_str(summary.get(label_key))
    #
    # if label:
    #     return label

    seconds = _optional_int(summary.get(seconds_key))

    return _format_duration_hh_mm(seconds=seconds)


def _format_duration_hh_mm(
    *,
    seconds: int | None,
) -> str:
    if seconds is None:
        return '--:--:--'

    safe_seconds = max(0, int(seconds))
    hours = safe_seconds // 3600
    minutes = safe_seconds % 3600 // 60
    remaining_seconds = safe_seconds % 60

    return f'{hours:02d}:{minutes:02d}:{remaining_seconds:02d}'


def _optional_int(value: Any) -> int | None:
    if value is None or value == '':
        return None

    try:
        return int(float(value))
    except Exception:
        return None


def _safe_str(value: Any) -> str:
    if value is None:
        return ''

    return str(value).strip()


def _as_dict(value: Any) -> dict[str, Any]:
    if isinstance(value, dict):
        return value

    return {}
