from __future__ import annotations

from src.features.configuration.models import (
    AdminSchema,
    FieldDefinition,
)

ALARM_IMAGE_CONFIGURATION_ADMIN_SCHEMA = AdminSchema(
    key='alarm_image_configuration',
    title='Configuración de Imágenes de Alarmas',
    fields=(
        FieldDefinition(
            name='message_group_key',
            label='Grupo de Mensajes',
            field_type='text',
            required=True,
            help_text='Grupo de alarmas al que pertenecen las imágenes.',
        ),
        FieldDefinition(
            name='image_key',
            label='Key Imagen',
            field_type='text',
            required=True,
            help_text='Identificador técnico estable de la imagen.',
        ),
        FieldDefinition(
            name='order',
            label='Orden',
            field_type='number',
            required=True,
            default_value=1,
        ),
        FieldDefinition(
            name='bundle_key',
            label='Bundle',
            field_type='text',
            required=True,
            default_value='bundle_001',
        ),
        FieldDefinition(
            name='bundle_hash',
            label='Hash Bundle',
            field_type='text',
            required=False,
        ),
        FieldDefinition(
            name='thumb_path',
            label='Ruta Thumb',
            field_type='text',
            required=True,
        ),
        FieldDefinition(
            name='full_path',
            label='Ruta Full',
            field_type='text',
            required=True,
        ),
        FieldDefinition(
            name='thumb_mime_type',
            label='MIME Thumb',
            field_type='text',
            required=True,
            default_value='image/webp',
        ),
        FieldDefinition(
            name='full_mime_type',
            label='MIME Full',
            field_type='text',
            required=True,
        ),
        FieldDefinition(
            name='content_hash',
            label='Hash Contenido',
            field_type='text',
            required=False,
        ),
    ),
)
