# Development Notes

## Requirements

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
