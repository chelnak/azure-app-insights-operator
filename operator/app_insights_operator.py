import kopf
from app_insights import app_insights
from utilities import kubernetes
from config import config as c


@kopf.on.create(c.GROUP, c.VERSION, c.PLURAL)
def create(meta, spec, namespace, logger, **kwargs):

    name = meta.get('name')

    resource_group = spec.get('resourcegroup')
    if not resource_group:
        raise kopf.PermanentError(
            f"Property resourcegroup must be set. Got {resource_group!r}."
        )

    location = spec.get('location')
    if not location:
        raise kopf.PermanentError(
            f"Property location must be set. Got {location!r}."
        )

    logger.info(f"Creating app insights resource: {name}.")
    resourceid, instrumentation_key = app_insights.create_or_update(
        resource_group,
        name,
        location,
        {'namespace': namespace}
    )

    logger.info("Creating child secret with instrumentation key.")
    kubernetes.create_namespaced_secret(instrumentation_key, name, namespace)

    logger.info(
        f"Application Insights {name} created."
    )

    return {
        'resourceid': resourceid,
        'instrumentationkey': instrumentation_key
    }


@kopf.on.delete(c.GROUP, c.VERSION, c.PLURAL)
def delete(meta, spec, logger, **kwargs):

    name = meta.get('name')

    resource_group = spec.get('resourcegroup')
    if not resource_group:
        raise kopf.PermanentError(
            f"Property resourcegroup must be set. Got {resource_group!r}."
        )

    location = spec.get('location')
    if not location:
        raise kopf.PermanentError(
            f"Property location must be set. Got {location!r}."
        )

    app_insights.delete(resource_group, name)
