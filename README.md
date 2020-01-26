[![Build Status](https://craigg.visualstudio.com/Pipelines/_apis/build/status/azure-app-insights-operator?branchName=master)](https://craigg.visualstudio.com/Pipelines/_build/latest?definitionId=21&branchName=master)

# Kubernetes Operator for Application Insights

> :construction: This project is experimental and may contain bugs

This is a Kuberetes operator for Azure Application insights. The goal of this operator is to aid in the development of .NET applications that use Applcation Insights for telemetry. It allows Application Insights to become a first class citizen inside the cluster and be configured and deployed alongside other Kubernetes resources.

When an Application Insights resource is deployed to a cluster the folowing will happen:

* A new Application Insights resource is deployed to the namespace that has been specified in the request.
* A new application Insights resource is deployed in to Azure using the information provided in the `spec` section of the manifest.
* An opaque secret is created that contains the instrumentation key of the deployed Application Insights resource. This can be linked to a deployment and consumed by your application.

The operator has been writen with [KOPF](https://github.com/zalando-incubator/kopf) created by [zalando](https://www.zalando.co.uk/).

## Installation

1. Install the default kopf peerings

```bash
kubectl apply -f resources/kopf-peering.yml -n engineering
```

2. Install custom resource definitions for the operator

```bash
kubectl apply -f resourcs/app_insights_operator_crd.yml -n engineering
```

3. Configure rbac for the operator

```bash
kubectl apply -f resourcs/app_insights_operator_rbac.yml -n engineering
```

4. Deploy the operator

```bash
kubectl apply -f resourcs/app_insights_operator_deployment.yml -n engineering
```

5. Deploy a test App Insights resource

```bash
kubectl apply -f resourcs/app_insights_resource.yml -n engineering
```

6. Validate the existence of the new resources:

```bash
kubectl get ai -n engineering
```

!["k8s-resource"](media/provisioned-resource.PNG)

```bash
kubectl get secrets -n engineering
```

!["k8s-secret"](media/provisioned-secret.PNG)

## Development

### Requirements

* python 3.8.1
* virtualenv
* docker
* Azure App Registration with enough permission to create, update and remove App Insights resources and Resource Groups in a subscription.
* Configure `devsetup.ps1`

```bash
virtualenv env
devsetup.ps1
kopf run .\operator\app_insights_operator.py --dev
```
