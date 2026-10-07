from __future__ import annotations

from src.features.configuration.models import (
    AdminSchema,
    FieldDefinition,
)

ALARM_IMAGE_BUNDLE_MANIFEST_ADMIN_SCHEMA = AdminSchema(
    key='alarm_image_bundle_manifest',
    title='Manifest Bundles de Imágenes de Alarmas',
    fields=(
        FieldDefinition(
            name='bundle_key',
            label='Bundle',
            field_type='text',
            required=True,
        ),
        FieldDefinition(
            name='bundle_hash',
            label='Hash Bundle',
            field_type='text',
            required=True,
        ),
        FieldDefinition(
            name='bundle_filename',
            label='Archivo Bundle',
            field_type='text',
            required=True,
        ),
        FieldDefinition(
            name='bundle_relative_path',
            label='Ruta SharePoint',
            field_type='text',
            required=True,
        ),
        FieldDefinition(
            name='size_bytes',
            label='Tamaño Bytes',
            field_type='number',
            required=True,
            default_value=0,
        ),
        FieldDefinition(
            name='message_group_keys_json',
            label='Message Groups',
            field_type='text',
            required=True,
            default_value='[]',
        ),
        FieldDefinition(
            name='updated_at',
            label='Actualizado',
            field_type='text',
            required=True,
        ),
        FieldDefinition(
            name='published_at',
            label='Publicado',
            field_type='text',
            required=False,
        ),
        FieldDefinition(
            name='published_by',
            label='Publicado Por',
            field_type='text',
            required=False,
        ),
        FieldDefinition(
            name='published_by_email',
            label='Email Publicador',
            field_type='text',
            required=False,
        ),
    ),
)
