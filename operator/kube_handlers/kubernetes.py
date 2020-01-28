import os
import yaml
import kubernetes
from kubernetes.client.rest import ApiException
import kopf
from base64 import b64encode


def parse_secret_template(name, instrumentation_key):
    encoded_instrumentation_key = b64encode(
        instrumentation_key.encode('utf8')).decode('utf8')

    path = os.path.join(os.path.dirname(__file__), 'templates/secret.yml')
    tmpl = open(path, 'rt').read()
    text = tmpl.format(
        name=name, instrumentationkey=encoded_instrumentation_key)

    return yaml.safe_load(text)


def create_namespaced_secret(instrumentation_key, name, namespace):
    try:
        client = kubernetes.client.CoreV1Api()
        body = parse_secret_template(name, instrumentation_key)
        client.create_namespaced_secret(
            namespace=namespace,
            body=body
        )

        kopf.info(
            body,
            reason="CREATED",
            message=f"Created secret {name} in namespace {namespace}")

    except ApiException as e:
        message = f"Failed to create secret {name}: {e.reason} | {e.status}"
        kopf.exception(
            body,
            reason=e.reason,
            message=message
        )

        raise kopf.PermanentError(message)


def patch_namespaced_secret(name, namespace, patch):
    try:
        client = kubernetes.client.CoreV1Api()
        client.patch_namespaced_secret(
            name=name,
            namespace=namespace,
            body=patch
        )

        kopf.info(
            patch,
            reason="UPDATED",
            message=f"Updated secret {name} in namespace {namespace}"
        )

    except ApiException as e:
        message = f"Failed to patch secret {name}: {e.reason} | {e.status}"
        kopf.exception(
            patch,
            reason=e.reason,
            message=message
        )
        raise kopf.PermanentError(message)
