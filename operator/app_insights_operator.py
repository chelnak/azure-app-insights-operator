import kopf
from app_insights import app_insights
from kube_handlers import kubernetes
from config import config as c


@kopf.on.create(c.GROUP, c.VERSION, c.PLURAL)
def create(meta, spec, namespace, logger, **kwargs):

    try:
        s = {}
        for k, v in spec.items():
            s[k] = v

        name = meta.get('name')
        resource_group = s.pop('resourcegroup')
        location = s.pop('location')

        labels = meta.get('labels', {})
        tags = {'k8s_namespace': namespace}
        for k, v in labels.items():
            tags[f"k8s_{k}"] = v

        logger.info(f"Creating app insights resource: {name}.")
        resourceid, instrumentation_key = app_insights.create_or_update(
            resource_name=name,
            resource_group_name=resource_group,
            location=location,
            tags=tags,
            spec=s
        )

        logger.info("Creating child secret with instrumentation key.")
        kubernetes.create_namespaced_secret(
            instrumentation_key, name, namespace)

        logger.info(
            f"Application Insights {name} created."
        )

        return {
            'name': name,
            'resourceid': resourceid,
            'instrumentationkey': instrumentation_key
        }
    except RuntimeError as e:
        raise kopf.PermanentError(
            f"Failed to create app insights resource {name}: {e}")


@kopf.on.update(c.GROUP, c.VERSION, c.PLURAL)
def update(name, spec, status, meta, namespace, logger, **kwargs):

    try:
        logger.info(f"status {status}")
        logger.info(f"meta {meta}")

        s = {}
        for k, v in spec.items():
            s[k] = v

        resource_group = s.pop('resourcegroup')
        location = s.pop('location')

        labels = meta.get('labels', {})
        tags = {'k8s_namespace': namespace}
        for k, v in labels.items():
            tags[f"k8s_{k}"] = v

        logger.info(f"Updating app insights resource: {name}.")
        resourceid, instrumentation_key = app_insights.create_or_update(
            resource_name=name,
            resource_group_name=resource_group,
            location=location,
            tags=tags,
            spec=s
        )

    except RuntimeError as e:
        raise kopf.PermanentError(
            f"Failed to update app insights resource {name}: {e}")


@kopf.on.field(c.GROUP, c.VERSION, c.PLURAL, field='metadata.labels')
def relabel(spec, status, namespace, old, new, logger, **kwargs):

    try:
        s = {}
        for k, v in spec.items():
            s[k] = v

        name = status.get('create').get('name')
        resource_group = s.pop('resourcegroup')
        location = s.pop('location')
        patch = {'metadata': {'labels': new}}

        kubernetes.patch_namespaced_secret(name, namespace, patch)

        tags = {}
        for k, v in new.items():
            tags[f"k8s_{k}"] = v

        logger.info(f"Updating app insights resource tags: {tags}.")
        resourceid, instrumentation_key = app_insights.create_or_update(
            resource_name=name,
            resource_group_name=resource_group,
            location=location,
            tags=tags,
            spec=s
        )

    except RuntimeError as e:
        raise kopf.PermanentError(
            f"Failed to relabel app insights resource {name}: {e}")


@kopf.on.delete(c.GROUP, c.VERSION, c.PLURAL)
def delete(meta, spec, logger, **kwargs):

    try:
        name = meta.get('name')
        resource_group = spec.get('resourcegroup')

        app_insights.delete(resource_group, name)

    except RuntimeError as e:
        raise kopf.PermanentError(
            f"Failed to delete app insights resource {name}: {e}")
