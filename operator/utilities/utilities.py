from azure.common.credentials import ServicePrincipalCredentials
from config.config import (
    AZURE_CLIENT_ID,
    AZURE_CLIENT_SECRET,
    AZURE_SUBSCRIPTION_ID,
    AZURE_TENANT_ID
)


def get_credentials():
    subscription_id = AZURE_SUBSCRIPTION_ID
    credentials = ServicePrincipalCredentials(
        client_id=AZURE_CLIENT_ID,
        secret=AZURE_CLIENT_SECRET,
        tenant=AZURE_TENANT_ID
    )
    return credentials, subscription_id
