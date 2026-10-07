from __future__ import annotations

from dash.development.base_component import Component
from dash import html
from src.shared.time.timestamps import parse_utc_datetime
from src.shared.ui.app_time_status_shell.model import AppTimeStatusShellGroupStructure, AppTimeStatusShellStructure
from typing import Any
from datetime import datetime
import pytz


_SECONDS_PER_MINUTE = 60
_SECONDS_PER_HOUR = 60 * 60
_SECONDS_PER_DAY = 24 * 60 * 60
_CRITICAL_TIME_SECONDS = 5 * 60
_CRITICAL_TIME_SECONDS_D = 10 * 60

def build_time_status_content(
    *,
    last_update_pi,
    last_update_dispatch = None
) -> Component:
    statuses = []
    for (label, _time, divisor, seconds) in [
        ('PI System', last_update_pi, True, _CRITICAL_TIME_SECONDS),
        ('Dispatch', last_update_dispatch, False, _CRITICAL_TIME_SECONDS_D),
    ]:
        icons_class_name, text, wrapper_class_name = _build_time_status(_time=_time, seconds=seconds)
        statuses.append(
            AppTimeStatusShellStructure(
                label=label,
                icon_class_name=icons_class_name,
                right_divisor=divisor,
                value=text,
                wrapper_class_name=wrapper_class_name,
            )
        )

    return AppTimeStatusShellGroupStructure(
        statuses_structure=tuple(statuses),
    ).to_component()


def _build_time_status(
    *,
    _time: Any,
    seconds: Any
):
    last_update = parse_utc_datetime(value=_time)

    if last_update is None:
        return (
            'bi bi-cloud-slash',
            html.Img(
                className='img-fluid invalid-value-icon',
                src='assets/img/icons/invalid_data.svg',
            ),
            'time-danger',
        )

    now = datetime.now(pytz.utc)

    elapsed_seconds = max(
        0,
        int((now - last_update).total_seconds()),
    )

    class_name_icon = 'bi bi-cloud-check'
    wrapper_class_name = ''

    if elapsed_seconds > seconds:
        class_name_icon = 'bi bi-cloud-slash'
        wrapper_class_name = 'time-danger'

    text = _format_elapsed_time(
        elapsed_seconds=elapsed_seconds,
    )

    return class_name_icon, text, wrapper_class_name


def _format_elapsed_time(
    *,
    elapsed_seconds: int,
) -> str:
    if elapsed_seconds < _SECONDS_PER_MINUTE:
        return _format_exact_elapsed_time(
            value=elapsed_seconds,
            singular_unit='segundo',
            plural_unit='segundos',
        )

    if elapsed_seconds < _SECONDS_PER_HOUR:
        minutes, remaining_seconds = divmod(
            elapsed_seconds,
            _SECONDS_PER_MINUTE,
        )

        return _format_elapsed_unit(
            value=minutes,
            remaining_value=remaining_seconds,
            singular_unit='minuto',
            plural_unit='minutos',
        )

    if elapsed_seconds < _SECONDS_PER_DAY:
        hours, remaining_seconds = divmod(
            elapsed_seconds,
            _SECONDS_PER_HOUR,
        )

        return _format_elapsed_unit(
            value=hours,
            remaining_value=remaining_seconds,
            singular_unit='hora',
            plural_unit='horas',
        )

    days, remaining_seconds = divmod(
        elapsed_seconds,
        _SECONDS_PER_DAY,
    )

    return _format_elapsed_unit(
        value=days,
        remaining_value=remaining_seconds,
        singular_unit='día',
        plural_unit='días',
    )


def _format_elapsed_unit(
    *,
    value: int,
    remaining_value: int,
    singular_unit: str,
    plural_unit: str,
) -> str:
    unit = singular_unit if value == 1 else plural_unit

    if remaining_value > 0:
        return f'hace más de {value} {unit}'

    return f'hace {value} {unit}'


def _format_exact_elapsed_time(
    *,
    value: int,
    singular_unit: str,
    plural_unit: str,
) -> str:
    unit = singular_unit if value == 1 else plural_unit
    return f'hace {value} {unit}'