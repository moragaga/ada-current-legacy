from __future__ import annotations

from src.features.alarm_management.domain import SILENCE_POLICY_CODES
from src.features.configuration.models import AdminSchema, FieldDefinition

ALARM_CONFIGURATION_ADMIN_SCHEMA = AdminSchema(
    key='alarm_configuration',
    title='Administración configuración de Alarmas',
    fields=(
        FieldDefinition(
            name='alarm_family_key',
            label='Familia de Alarma',
            field_type='text',
            required=True,
            help_text='Agrupador técnico general. Ejemplo: nivel_espuma, h2s, ph, orp.',
        ),
        FieldDefinition(
            name='alarm_key',
            label='Key Alarma',
            field_type='text',
            required=True,
            help_text='Identificador único de la alarma. Debe coincidir con la key técnica del runtime.',
        ),
        FieldDefinition(
            name='alarm_display_name',
            label='Nombre Visible',
            field_type='text',
            required=True,
            help_text='Nombre corto y amigable para tarjetas, dashboards, listados y feedback.',
        ),
        FieldDefinition(
            name='message_group_key',
            label='Grupo de Mensajes',
            field_type='text',
            required=True,
            help_text='Grupo usado para resolver mensajes predefinidos del modal.',
        ),
        FieldDefinition(
            name='visibility_group_key',
            label='Grupo Visual',
            field_type='text',
            required=True,
            help_text='Grupo usado por el runtime para visualización/agrupación.',
        ),
        FieldDefinition(
            name='management_scope_key',
            label='Scope Gestión',
            field_type='text',
            required=True,
            help_text='Scope técnico de gestión. Normalmente igual al grupo visual.',
        ),
        FieldDefinition(
            name='operator_bucket',
            label='Bucket Operador',
            field_type='text',
            required=True,
            default_value='default',
            help_text='Bucket operativo del front. Usar default salvo casos especiales como h2s.',
        ),
        FieldDefinition(
            name='modal_title',
            label='Título Modal',
            field_type='text',
            required=True,
        ),
        FieldDefinition(
            name='alarm_kind',
            label='Tipo de Alarma',
            field_type='text',
            required=True,
            help_text='Ejemplo: Riesgo Productivo, Impacto Seguridad y Salud.',
        ),
        FieldDefinition(
            name='title',
            label='Título Alarma',
            field_type='text',
            required=True,
        ),
        FieldDefinition(
            name='cause',
            label='Causa',
            field_type='text',
            required=True,
        ),
        FieldDefinition(
            name='color',
            label='Color',
            field_type='select',
            options=('yellow', 'red', 'blue'),
            required=True,
            default_value='yellow',
        ),
        FieldDefinition(
            name='default_silence_policy_code',
            label='Política Silencio Base',
            field_type='select',
            options=SILENCE_POLICY_CODES,
            required=True,
            default_value='none',
            help_text=(
                'none = no silencia; h01-h11 = horas; '
                'shift_end = hasta fin de turno; inherit se reserva para mensajes.'
            ),
        ),
        FieldDefinition(
            name='allow_manual_silence',
            label='Permite Silencio Manual',
            field_type='boolean',
            required=True,
            default_value=True,
            help_text='Permite que una gestión con mensaje personalizado pueda solicitar silencio.',
        ),
        FieldDefinition(
            name='allow_management',
            label='Permite Gestión',
            field_type='boolean',
            required=True,
            default_value=True,
        ),
        FieldDefinition(
            name='visible',
            label='Visible',
            field_type='boolean',
            required=True,
            default_value=True,
        ),
        FieldDefinition(
            name='enabled',
            label='Ejecutar',
            field_type='boolean',
            required=True,
            default_value=True,
        ),
        FieldDefinition(
            name='priority_order',
            label='Prioridad',
            field_type='number',
            required=True,
            default_value=999,
        ),
        FieldDefinition(
            name='cascade_management_to_lower_priorities',
            label='Cascada a menor prioridad',
            field_type='boolean',
            required=True,
            default_value=True,
            help_text='Permite que una gestión afecte alarmas de menor prioridad dentro del mismo scope.',
        ),
    ),
)
