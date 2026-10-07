from __future__ import annotations

from dash import html

from ...mappers.remanentes import build_remanentes_metrics_mapper, build_remanentes_summary_mapper


def build_remanentes_content(kpis: dict):
    summary = build_remanentes_summary_mapper(kpis=kpis)
    metrics = build_remanentes_metrics_mapper(kpis=kpis)

    return html.Div(
        className='d-flex flex-column gap-1',
        children=[summary.to_component(), *metrics.to_components()],
    )
