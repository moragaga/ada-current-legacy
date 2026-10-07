from __future__ import annotations

from azure.cosmos import CosmosClient

from .settings import CosmosSettings


def ensure_required_database(client: CosmosClient, settings: CosmosSettings) -> None:
    try:
        client.create_database_if_not_exists(settings.database_name)
    except Exception as e:
        raise ValueError(
            f'[ERROR] The database {settings.database_name} cannot be created: {e}'
        ) from e
