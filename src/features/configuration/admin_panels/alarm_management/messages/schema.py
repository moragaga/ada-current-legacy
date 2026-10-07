from __future__ import annotations

from src.features.alarm_management.domain import SILENCE_POLICY_CODES
from src.features.configuration.models import AdminSchema, FieldDefinition

ALARM_MANAGEMENT_MESSAGE_ROW_SCHEMA = AdminSchema(
    key='alarm_management_message_row',
    title='Mensajes de gestión de alarmas',
    fields=(
        FieldDefinition(
            name='message_id',
            label='ID técnico',
            field_type='text',
            required=False,
            editable=False,
        ),
        FieldDefinition(
            name='message',
            label='Mensaje',
            field_type='text',
            required=True,
        ),
        FieldDefinition(
            name='silence_policy_code',
            label='Política de silencio',
            field_type='select',
            options=SILENCE_POLICY_CODES,
            required=True,
            default_value='inherit',
        ),
        FieldDefinition(
            name='allow_silence_edit',
            label='Permite editar silencio',
            field_type='boolean',
            required=True,
            default_value=True,
        ),
        FieldDefinition(
            name='is_active',
            label='Activo',
            field_type='boolean',
            required=True,
            default_value=True,
        ),
        FieldDefinition(
            name='sort_order',
            label='Orden',
            field_type='number',
            required=False,
            editable=False,
            default_value=0,
        ),
    ),
)
