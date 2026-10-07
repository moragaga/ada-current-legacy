from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

AlarmManagementFeedbackKind = Literal[
    'success',
    'error',
    'empty',
    'exists',
    'management_disabled',
    'validation_error',
]


@dataclass(frozen=True)
class AlarmManagementFeedbackViewModel:
    is_open: bool = False
    kind: AlarmManagementFeedbackKind = 'success'
    title: str = ''
    message: str = ''

    @classmethod
    def closed(cls) -> AlarmManagementFeedbackViewModel:
        return cls(is_open=False)


@dataclass(frozen=True)
class AlarmManagementModalViewModel:
    is_open: bool
    context_data: dict[str, Any] | None

    alarm_id: str = ''
    group_occurrence_id: str = ''
    alarm_key: str = ''

    visibility_group_key: str = ''
    management_scope_key: str = ''
    priority_order: int | None = None
    operator_bucket: str = 'default'

    target_occurrence_started_at: str = ''

    modal_title: str = ''
    alarm_title: str = ''
    alarm_cause: str = ''
    alarm_color: str = 'yellow'

    warning_message: str | None = None
    warning_class_name: str = 'd-none'

    message_options: list[dict[str, str]] = field(default_factory=list)
    messages_by_id: dict[str, dict[str, Any]] = field(default_factory=dict)

    silence_options: list[dict[str, str]] = field(default_factory=list)
    silence_disabled: bool = True
    silence_container_class_name: str = 'd-none'
    silence_information: str = ''

    selected_message_id: str | None = None
    personalized_message: str = ''
    silence_requested: bool = False
    selected_silence_policy_code: str | None = None

    @classmethod
    def closed(cls) -> AlarmManagementModalViewModel:
        return cls(
            is_open=False,
            context_data=None,
        )


@dataclass(frozen=True)
class AlarmManagementModalPresentation:
    modal: AlarmManagementModalViewModel
    feedback: AlarmManagementFeedbackViewModel

    @classmethod
    def closed(cls) -> AlarmManagementModalPresentation:
        return cls(
            modal=AlarmManagementModalViewModel.closed(),
            feedback=AlarmManagementFeedbackViewModel.closed(),
        )
