from __future__ import annotations

from dash import dcc, html

from ..components.alarm_management_feedback_modal import build_alarm_management_feedback_modal
from ..components.alarm_management_modal import build_alarm_management_modal
from ..ids import build_alarm_management_operator_ids


def build_alarm_management_modal_host() -> html.Div:
    ids = build_alarm_management_operator_ids()

    return html.Div(
        children=[
            dcc.Store(
                id=ids['context_store'],
                data=None,
                storage_type='memory',
            ),
            dcc.Store(
                id=ids['feedback_store'],
                data=None,
                storage_type='memory',
            ),
            dcc.Store(
                id=ids['validation_attempt_store'],
                data=False,
                storage_type='memory',
            ),
            build_alarm_management_modal(),
            build_alarm_management_feedback_modal(),
        ],
    )
