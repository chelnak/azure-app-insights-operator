import os
import yaml
import kubernetes
import kopf
from base64 import b64encode


def create_namespaced_secret(instrumentation_key, name, namespace):
    encoded_instrumentation_key = b64encode(
        instrumentation_key.encode('utf8')).decode('utf8')

    path = os.path.join(os.path.dirname(__file__), 'templates\\secret.yml')
    tmpl = open(path, 'rt').read()
    text = tmpl.format(
        name=name, instrumentationkey=encoded_instrumentation_key)
    data = yaml.safe_load(text)

    kopf.adopt(data)

    api = kubernetes.client.CoreV1Api()
    api.create_namespaced_secret(
        namespace=namespace,
        body=data,
    )
