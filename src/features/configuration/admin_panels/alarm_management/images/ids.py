from __future__ import annotations


class AlarmImageDefinitionIds:
    ROOT = 'alarm-image-definition-root'

    INIT_TRIGGER = 'alarm-image-definition-init-trigger'
    TRIGGER_LISTENER = 'alarm-image-definition-trigger-listener'
    STORE_DRAFT = 'alarm-image-definition-draft-store'

    # STATUS_BANNER = 'alarm-image-definition-status-banner'
    SEARCH_INPUT = 'alarm-image-definition-search-input'

    GROUP_LIST = 'alarm-image-definition-group-list'
    GROUP_PREVIOUS_PAGE = 'alarm-image-definition-group-previous-page'
    GROUP_NEXT_PAGE = 'alarm-image-definition-group-next-page'
    GROUP_PAGE_LABEL = 'alarm-image-definition-group-page-label'

    IMAGE_PANEL = 'alarm-image-definition-image-panel'
    PUBLISH_BUTTON = 'alarm-image-definition-publish-button'
    REFRESH_BUTTON = 'alarm-image-definition-refresh-button'

    GROUP_CARD = 'alarm-image-definition-group-card'
    ADD_IMAGE_UPLOAD = 'alarm-image-definition-add-image-upload'
    IMAGE_MOVE_UP = 'alarm-image-definition-image-move-up'
    IMAGE_MOVE_DOWN = 'alarm-image-definition-image-move-down'
    IMAGE_DELETE = 'alarm-image-definition-image-delete'
    IMAGE_REPLACE_UPLOAD = 'alarm-image-definition-image-replace-upload'

    MONITOR = 'alarm-image-definition-monitor'

    MAIN_LOADER = 'alarm-image-definition-loader'
    MAIN_DEFINITION_SHELL = 'alarm-image-definition-shell'

    @staticmethod
    def group_card(message_group_key: str) -> dict[str, str]:
        return {
            'type': AlarmImageDefinitionIds.GROUP_CARD,
            'message_group_key': message_group_key,
        }

    @staticmethod
    def add_image_upload(message_group_key: str) -> dict[str, str]:
        return {
            'type': AlarmImageDefinitionIds.ADD_IMAGE_UPLOAD,
            'message_group_key': message_group_key,
        }

    @staticmethod
    def image_move_up(message_group_key: str, image_key: str) -> dict[str, str]:
        return {
            'type': AlarmImageDefinitionIds.IMAGE_MOVE_UP,
            'message_group_key': message_group_key,
            'image_key': image_key,
        }

    @staticmethod
    def image_move_down(message_group_key: str, image_key: str) -> dict[str, str]:
        return {
            'type': AlarmImageDefinitionIds.IMAGE_MOVE_DOWN,
            'message_group_key': message_group_key,
            'image_key': image_key,
        }

    @staticmethod
    def image_delete(message_group_key: str, image_key: str) -> dict[str, str]:
        return {
            'type': AlarmImageDefinitionIds.IMAGE_DELETE,
            'message_group_key': message_group_key,
            'image_key': image_key,
        }

    @staticmethod
    def image_replace_upload(message_group_key: str, image_key: str) -> dict[str, str]:
        return {
            'type': AlarmImageDefinitionIds.IMAGE_REPLACE_UPLOAD,
            'message_group_key': message_group_key,
            'image_key': image_key,
        }
