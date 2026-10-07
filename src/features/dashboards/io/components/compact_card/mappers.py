from __future__ import annotations

from typing import Any

from .definitions import (
    CompactCardDefinition,
    CompactCardGroupDefinition,
    CompactCardRowDefinition,
)
from .models import (
    CompactCardData,
    CompactCardGroupData,
    CompactCardRowData,
    CompactCardTitleData,
    CompactCardValueData,
)


def map_to_compact_card_rows(
    *,
    definition: CompactCardRowDefinition,
    kpis: dict[str, Any],
) -> CompactCardRowData:
    return CompactCardRowData(
        rows=tuple(
            map_to_compact_card_group(
                definitions=definitions,
                kpis=kpis,
            )
            for definitions in definition.rows
        )
    )


def map_to_compact_card_group(
    *,
    definitions: CompactCardGroupDefinition,
    kpis: dict[str, Any],
) -> CompactCardGroupData:
    return CompactCardGroupData.from_iterable(
        indicator=definitions.indicator,
        indicator_position=definitions.indicator_position,
        wrapper_class_name=definitions.wrapper_class_name,
        cards=(
            map_to_compact_card(
                definition=definition,
                kpis=kpis,
            )
            for definition in definitions.cards
        ),
    )


def map_to_compact_card(
    *,
    definition: CompactCardDefinition,
    kpis: dict[str, Any],
) -> CompactCardData:
    return CompactCardData(
        title=CompactCardTitleData(
            label=definition.title.label,
            label_class_name=definition.title.label_class_name,
            extra_label=definition.title.extra_label,
            extra_label_class_name=definition.title.extra_label_class_name,
        ),
        values=tuple(
            CompactCardValueData(
                label=value.label,
                label_class_name=value.label_class_name,
                value=kpis.get(value.value_key),
                value_class_name=value.value_class_name,
                color=kpis.get(value.color_key),
            )
            for value in definition.values
        ),
        wrapper_class_name=definition.wrapper_class_name,
        card_color=kpis.get(definition.card_color_key),
    )
