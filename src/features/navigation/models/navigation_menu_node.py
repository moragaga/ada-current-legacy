from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

from .navigation_group import NavigationGroup
from .navigation_link import NavigationLink

NavigationMenuNodeType = Literal['link', 'group']


@dataclass(frozen=True)
class NavigationMenuNode:
    node_type: NavigationMenuNodeType
    order: int
    link: NavigationLink | None = None
    group: NavigationGroup | None = None
    children: tuple[NavigationLink, ...] = field(default_factory=tuple)

    @staticmethod
    def from_link(link: NavigationLink) -> NavigationMenuNode:
        return NavigationMenuNode(
            node_type='link',
            order=link.order,
            link=link,
        )

    @staticmethod
    def from_group(
        group: NavigationGroup,
        children: tuple[NavigationLink, ...],
    ) -> NavigationMenuNode:
        return NavigationMenuNode(
            node_type='group',
            order=group.order,
            group=group,
            children=children,
        )
