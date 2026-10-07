from __future__ import annotations

import logging

from azure.cosmos import CosmosClient

from .settings import CosmosSettings

logger = logging.getLogger(__name__)


def create_cosmos_client(settings: CosmosSettings) -> CosmosClient:
    if not settings.account_uri:
        raise ValueError('[ERROR] COSMOS_ACCOUNT_URI is required')
    if not settings.account_key:
        raise ValueError('[ERROR] COSMOS_ACCOUNT_KEY is required')

    try:
        additional_parameters = {'connection_mode': 'Gateway'} if settings.use_gateway else {}
        client = CosmosClient(
            url=settings.account_uri, credential=settings.account_key, **additional_parameters
        )
        logger.info('Cosmos client created successfully')
        return client
    except Exception as e:
        logger.exception(f'Failed to create cosmos client. Exception: {e}')
