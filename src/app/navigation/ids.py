from __future__ import annotations


class AppNavigationIds:
    HEADER_LOCATION = 'app-header-location'
    HEADER_OFFCANVAS = 'app-header-offcanvas'
    HEADER_MENU_CONTENT = 'app-header-menu-content'
    HEADER_MOBILE_TOGGLE = 'app-header-mobile-toggle'
    HEADER_DESKTOP_TOGGLE = 'app-header-desktop-toggle'
    HEADER_CLOSE_TRIGGER = 'app-header-close-trigger'

    NAVIGATION_GROUP_TOGGLE = 'app-navigation-group-toggle'
    NAVIGATION_GROUP_COLLAPSE = 'app-navigation-group-collapse'

    @staticmethod
    def build_group_toggle_id(group_key: str) -> dict:
        return {
            'type': AppNavigationIds.NAVIGATION_GROUP_TOGGLE,
            'group_key': group_key,
        }

    @staticmethod
    def build_group_collapse_id(group_key: str) -> dict:
        return {
            'type': AppNavigationIds.NAVIGATION_GROUP_COLLAPSE,
            'group_key': group_key,
        }
