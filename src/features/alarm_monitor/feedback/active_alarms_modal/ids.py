from __future__ import annotations


class ActiveAlarmsModalIds:
    OPEN_BUTTON = 'active-alarms-modal-open-button'
    MODAL = 'active-alarms-modal'
    CLOSE_BUTTON = 'active-alarms-modal-close-button'

    FROZEN_SNAPSHOT_STORE = 'active-alarms-modal-frozen-snapshot-store'

    OPERATOR_PAGE_STORE = 'active-alarms-modal-operator-page-store'
    TRACKING_PAGE_STORE = 'active-alarms-modal-tracking-page-store'

    SEARCH_INPUT = 'active-alarms-modal-search-input'
    SORT_SELECT_TIME = 'active-alarms-modal-sort-select-time'
    FILTER_SELECT_CRITICITY = 'active-alarms-modal-sort-select-criticity'
    REFRESH_BUTTON = 'active-alarms-modal-refresh-button'

    LAST_UPDATED_TEXT = 'active-alarms-modal-last-updated-text'

    OPERATOR_COUNT = 'active-alarms-modal-operator-count'
    OPERATOR_LIST = 'active-alarms-modal-operator-list'
    OPERATOR_PREVIOUS_BUTTON = 'active-alarms-modal-operator-previous-button'
    OPERATOR_NEXT_BUTTON = 'active-alarms-modal-operator-next-button'
    OPERATOR_PAGE_TEXT = 'active-alarms-modal-operator-page-text'

    TRACKING_COUNT = 'active-alarms-modal-tracking-count'
    TRACKING_LIST = 'active-alarms-modal-tracking-list'
    TRACKING_PREVIOUS_BUTTON = 'active-alarms-modal-tracking-previous-button'
    TRACKING_NEXT_BUTTON = 'active-alarms-modal-tracking-next-button'
    TRACKING_PAGE_TEXT = 'active-alarms-modal-tracking-page-text'

    MANAGE_BUTTON_TYPE = 'active-alarms-modal-manage-button'

    PAGE_SIZE = 10

    @staticmethod
    def build_manage_button_id(*, row_id: str) -> dict[str, str]:
        return {
            'type': ActiveAlarmsModalIds.MANAGE_BUTTON_TYPE,
            'row_id': row_id,
        }
