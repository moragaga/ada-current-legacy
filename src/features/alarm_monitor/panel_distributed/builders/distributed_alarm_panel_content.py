from __future__ import annotations

from dash import html

from ...components.alarm_connectors.figures import (
    build_alarm_connectors_graph,
)
from ..components.distributed_alarm_card import build_distributed_alarm_card
from ..mappers.distributed_alarm_panel_mapper import (
    map_distributed_alarm_panel_view_model,
)


def build_distributed_alarm_panel_content(
    *,
    alarm_context: dict,
):
    model = map_distributed_alarm_panel_view_model(
        alarm_context=alarm_context,
    )

    occupied_slot_indexes = [index for index, slot in enumerate(model.slots) if slot is not None]

    return html.Div(
        className='alarm-panel-content',
        children=[
            html.Div(
                className='alarm-panel-slots',
                children=[
                    html.Div(
                        className=(
                            'alarm-panel-slot '
                            + (
                                'alarm-panel-slot-occupied'
                                if slot is not None
                                else 'alarm-panel-slot-empty'
                            )
                        ),
                        children=[
                            build_distributed_alarm_card(
                                alarm=slot,
                                bulk_group=model.bulk_group,
                            )
                        ]
                        if slot is not None
                        else [],
                    )
                    for slot in model.slots
                ],
            ),
            build_alarm_connectors_graph(
                occupied_slot_indexes=occupied_slot_indexes,
                total_slots=6,
            ),
        ],
    )
