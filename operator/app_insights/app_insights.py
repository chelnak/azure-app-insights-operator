from utilities import utilities
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.applicationinsights import ApplicationInsightsManagementClient
from azure.mgmt.applicationinsights.models import (
    ApplicationInsightsComponent,
    ApplicationType
)


def create_or_update(resource_group_name, resource_name, location, tags):

    credentials, subscription_id = utilities.get_credentials()

    resource_mangemnt_client = ResourceManagementClient(
        credentials,
        subscription_id
    )

    appinsights_client = ApplicationInsightsManagementClient(
        credentials,
        subscription_id
    )

    resource_group_params = {'location': location, 'tags': tags}
    resource_mangemnt_client.resource_groups.create_or_update(
        resource_group_name,
        resource_group_params
    )

    resource = appinsights_client.components.create_or_update(
        resource_group_name,
        resource_name,
        ApplicationInsightsComponent(
            location=location,
            kind="web",
            application_type=ApplicationType.web,
            tags=tags
        )
    )

    return (
        resource.id,
        resource.instrumentation_key
    )


def delete(resource_group_name, resource_name):

    credentials, subscription_id = utilities.get_credentials()

    appinsights_client = ApplicationInsightsManagementClient(
        credentials,
        subscription_id
    )

    appinsights_client.components.delete(resource_group_name, resource_name)
