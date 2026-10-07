from __future__ import annotations

from dash import html
from dash.development.base_component import Component

from src.shared.ui.app_dashboard_shell.runtime.stores import (
    build_dashboard_io_runtime_store_components,
)

from .ids import DashboardShellIOIds
from .models import DashboardShellIODefinition


def build_dashboard_io_layout(
    *,
    dashboard_definition: DashboardShellIODefinition,
    **kwargs,
):
    regions = _resolve_regions(**kwargs)

    header_region = regions.pop('header_region', [])
    alarm_region = regions.pop('alarm_region', [])

    dashboard = html.Div(
        id=DashboardShellIOIds.ROOT,
        children=[
            html.Header(
                id=DashboardShellIOIds.HEADER,
                children=header_region,
            ),
            html.Div(
                id=DashboardShellIOIds.ALARMS,
                children=alarm_region,
            ),
            html.Main(
                id=DashboardShellIOIds.BODY,
                children=_build_content(regions=regions),
            ),
        ],
    )

    return [
        *build_dashboard_io_runtime_store_components(
            interval_ms=dashboard_definition.dashboard_interval_ms,
        ),
        html.Div(
            id='main-page-loader-scope',
            **{
                'data-page-loader': 'true',
                'data-loader-key': 'main-dashboard',
            },
            children=[
                html.Div(
                    className='page-loader-content',
                    children=[dashboard],
                ),
                # html.Div(
                #     className='page-loader-overlay',
                #     children=[
                #         html.Div(
                #             className='page-loader-media-frame',
                #             children=[
                #                 html.Img(
                #                     className='page-loader-gif',
                #                     src='/assets/img/branding/loaders/loader.gif',
                #                 ),
                #                 html.Video(
                #                     className='page-loader-video',
                #                     autoPlay=True,
                #                     loop=True,
                #                     muted=True,
                #                     playsInline=True,
                #                     preload='auto',
                #                     children=[
                #                         html.Source(
                #                             src='/assets/img/branding/loaders/loader.mp4',
                #                             type='video/mp4',
                #                         )
                #                     ],
                #                 ),
                #             ],
                #         )
                #     ],
                # ),
            ],
        ),
    ]


def _resolve_regions(**kwargs) -> dict:
    regions: dict = {}

    for key, value in kwargs.items():
        if key.endswith('_region'):
            regions[key] = value or []

    return regions


def _build_content(*, regions: dict) -> Component:
    return html.Div(
        className='dashboard-io-main-wrapper-container',
        children=[
            html.Div(
                className='dashboard-io-main-mina-wrapper-container',
                children=[
                    _build_slot_content(
                        content_id=DashboardShellIOIds.GENERAL_MINA_REGION,
                        region=regions.pop('first_region', []),
                    ),
                    _build_second_slot_content(
                        second_region=regions.pop('second_region', []),
                        third_region=regions.pop('third_region', []),
                        middle_region=regions.pop('second_third_middle_region', []),
                    ),
                    _build_slot_content(
                        content_id=DashboardShellIOIds.CHANCADO_STMG_REGION,
                        region=regions.pop('fourth_region', []),
                    ),
                ],
            ),
            html.Div(
                className='dashboard-io-main-plant-wrapper-container',
                children=_build_plant_slots_content(regions=regions),
            ),
        ],
    )


def _build_slot_content(
    *,
    content_id: str,
    region: list,
) -> Component:
    return html.Div(
        id=content_id,
        className='dashboard-io-region-slot d-flex flex-fill',
        children=region,
    )


def _build_second_slot_content(
    *,
    second_region: list,
    third_region: list,
    middle_region: list,
) -> Component:
    return html.Div(
        className='dashboard-io-main-wrapper-middle-container d-flex flex-fill',
        children=[
            html.Div(
                className='dashboard-io-main-wrapper-middle-top-container d-flex flex-fill',
                children=[
                    _build_slot_content(
                        content_id=DashboardShellIOIds.CARGUIO_REGION,
                        region=second_region,
                    ),
                    _build_slot_content(
                        content_id=DashboardShellIOIds.TRANSPORTE_REGION,
                        region=third_region,
                    ),
                ],
            ),
            _build_slot_content(
                content_id=DashboardShellIOIds.CARGUIO_TRANSPORTE_REGION,
                region=middle_region,
            ),
        ],
    )


def _build_plant_slots_content(*, regions: dict) -> list[Component]:
    return [
        _build_slot_content(
            content_id=content_id,
            region=regions.pop(region_key, []),
        )
        for region_key, content_id in _get_plant_region_entries()
    ]


def _get_plant_region_entries() -> tuple[tuple[str, str], ...]:
    return (
        ('fifth_region', DashboardShellIOIds.STOCK_CHACAY_REGION),
        ('sixth_region', DashboardShellIOIds.MOLIENDA_REGION),
        ('seventh_region', DashboardShellIOIds.FLOTACION_REGION),
        ('eighth_region', DashboardShellIOIds.TRANSPORTE_FLUIDOS_REGION),
        ('ninth_region', DashboardShellIOIds.PUERTO_REGION),
    )
