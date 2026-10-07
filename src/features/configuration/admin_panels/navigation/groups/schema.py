from __future__ import annotations

from src.features.configuration.models import AdminSchema, FieldDefinition, Profile

NAVIGATION_GROUPS_ADMIN_SCHEMA = AdminSchema(
    key='navigation_groups',
    title='Administración de grupos de navegación',
    fields=(
        FieldDefinition(
            name='group_id',
            label='ID',
            field_type='text',
            required=True,
            editable=False,
            help_text='Identificador técnico automático.',
        ),
        FieldDefinition(
            name='label',
            label='Etiqueta',
            field_type='text',
            required=True,
            help_text='Texto visible en el menú. Ejemplo: Administración',
        ),
        FieldDefinition(
            name='icon',
            label='Icono',
            field_type='text',
            required=False,
            help_text='Clase de Bootstrap Icons. Ejemplo: bi bi-gear',
        ),
        FieldDefinition(
            name='order',
            label='Orden',
            field_type='number',
            required=True,
            default_value=0,
            help_text='Orden del grupo en el menú principal. Recomendado usar 10, 20, 30...',
        ),
        FieldDefinition(
            name='visible_in_menu',
            label='Visible en menú',
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
            name='allow_profiles',
            label='Perfiles',
            field_type='semicolon_list',
            required=True,
            editable=True,
            options=Profile.values(),
            default_value='',
            help_text='Separar perfiles con ;. Las páginas hijas pueden heredar estos perfiles.',
        ),
    ),
)
