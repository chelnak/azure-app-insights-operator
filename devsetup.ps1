$PythonEnvironment = @{
    AZURE_SUBSCRIPTION_ID = "7db81549-e1e7-467b-9c24-04b81630eeaa"
    AZURE_CLIENT_ID = "0aea8535-1098-4bf3-b719-556dd8c5e65e"
    AZURE_CLIENT_SECRET = (Get-Content -Path "$PSScriptRoot/azure-secret.txt" -Raw)
    AZURE_TENANT_ID = "7a72e127-4c27-4128-88a2-f854ee260ef7"
}

$PythonEnvironment.Keys | ForEach-Object {
    New-Item -Path ENV:\$_ -Value $PythonEnvironment[$_] -Force
}

& "$PSScriptRoot\env\Scripts\activate.ps1"