from __future__ import annotations

PAGE_SIZE = 10

DEFAULT_SORT_ORDER = 'recent'
DEFAULT_CRITICITY_FILTER = 'all'
DEFAULT_STATUS_FILTER = 'all'
DEFAULT_TURN_SCOPE_FILTER = 'current'
DEFAULT_RECURRENCE_MIN_DURATION = '10'

TURN_SCOPE_ALL = 'all'
TURN_SCOPE_CURRENT = 'current'
TURN_SCOPE_PREVIOUS = 'previous'

RECURRENCE_MIN_DURATION_OPTIONS = [
    {'label': 'Todas', 'value': '0'},
    {'label': '≥ 5 min', 'value': '5'},
    {'label': '≥ 10 min', 'value': '10'},
    {'label': '≥ 15 min', 'value': '15'},
    {'label': '≥ 30 min', 'value': '30'},
]

ITEMS_CONTENT_SIDE_SHOW_CLASSNAME = 'managed-alarms-side-column d-flex flex-fill'
ITEMS_CONTENT_SIDE_HIDE_CLASSNAME = 'd-none'
ZOOM_IN_CONTENT_MAIN_BUTTON_CLASSNAME = (
    'bi bi-arrows-angle-expand managed-alarms-panel-icon active-cursor zoom-content-main-inactive'
)
ZOOM_OUT_CONTENT_MAIN_BUTTON_CLASSNAME = (
    'bi bi-arrows-angle-contract managed-alarms-panel-icon active-cursor zoom-content-main-active'
)
