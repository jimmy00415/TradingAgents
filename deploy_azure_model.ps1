# Deploy Azure OpenAI Model via Azure CLI
# This script deploys gpt-4o model to your Azure OpenAI resource

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Azure OpenAI Model Deployment Script" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan

# Configuration from your Azure resource
$resourceName = "Jimmy00415"
$resourceGroup = "TradingAgent"
$deploymentName = "gpt-4o"
$modelName = "gpt-4o"
$modelVersion = "2024-11-20"  # Latest stable version
$modelFormat = "OpenAI"
$skuCapacity = "1"
$skuName = "Standard"

Write-Host "`nConfiguration:" -ForegroundColor Yellow
Write-Host "  Resource Name: $resourceName"
Write-Host "  Resource Group: $resourceGroup"
Write-Host "  Deployment Name: $deploymentName"
Write-Host "  Model: $modelName (version $modelVersion)"
Write-Host "  SKU: $skuName (capacity: $skuCapacity)"

# Check if Azure CLI is installed
Write-Host "`n1. Checking Azure CLI installation..." -ForegroundColor Yellow
try {
    $azVersion = az version --output json 2>$null | ConvertFrom-Json
    Write-Host "   ✓ Azure CLI installed: $($azVersion.'azure-cli')" -ForegroundColor Green
} catch {
    Write-Host "   ✗ Azure CLI not found!" -ForegroundColor Red
    Write-Host "`n   Please install Azure CLI from: https://aka.ms/installazurecliwindows" -ForegroundColor Yellow
    exit 1
}

# Check if logged in
Write-Host "`n2. Checking Azure CLI login status..." -ForegroundColor Yellow
try {
    $account = az account show --output json 2>$null | ConvertFrom-Json
    if ($account) {
        Write-Host "   ✓ Logged in as: $($account.user.name)" -ForegroundColor Green
        Write-Host "   Subscription: $($account.name)" -ForegroundColor Cyan
    } else {
        Write-Host "   ✗ Not logged in to Azure" -ForegroundColor Red
        Write-Host "`n   Logging in..." -ForegroundColor Yellow
        az login
        if ($LASTEXITCODE -ne 0) {
            Write-Host "   ✗ Login failed" -ForegroundColor Red
            exit 1
        }
    }
} catch {
    Write-Host "   ✗ Not logged in to Azure" -ForegroundColor Red
    Write-Host "`n   Logging in..." -ForegroundColor Yellow
    az login
}

# Check if deployment already exists
Write-Host "`n3. Checking existing deployments..." -ForegroundColor Yellow
try {
    $existingDeployments = az cognitiveservices account deployment list `
        --name $resourceName `
        --resource-group $resourceGroup `
        --output json 2>$null | ConvertFrom-Json
    
    if ($existingDeployments) {
        Write-Host "   Found $($existingDeployments.Count) existing deployment(s):" -ForegroundColor Cyan
        foreach ($dep in $existingDeployments) {
            Write-Host "     - $($dep.name) ($($dep.properties.model.name))" -ForegroundColor Gray
            if ($dep.name -eq $deploymentName) {
                Write-Host "`n   ⚠ Deployment '$deploymentName' already exists!" -ForegroundColor Yellow
                $continue = Read-Host "   Do you want to delete and recreate it? (y/N)"
                if ($continue -eq 'y' -or $continue -eq 'Y') {
                    Write-Host "   Deleting existing deployment..." -ForegroundColor Yellow
                    az cognitiveservices account deployment delete `
                        --name $resourceName `
                        --resource-group $resourceGroup `
                        --deployment-name $deploymentName `
                        --output none
                    Write-Host "   ✓ Deleted" -ForegroundColor Green
                } else {
                    Write-Host "`n   Using existing deployment." -ForegroundColor Green
                    Write-Host "`n============================================================" -ForegroundColor Cyan
                    Write-Host "Deployment Name: $deploymentName" -ForegroundColor Green
                    Write-Host "============================================================" -ForegroundColor Cyan
                    exit 0
                }
            }
        }
    } else {
        Write-Host "   No existing deployments found" -ForegroundColor Gray
    }
} catch {
    Write-Host "   Could not list deployments (might be first time)" -ForegroundColor Gray
}

# Create the deployment
Write-Host "`n4. Creating model deployment..." -ForegroundColor Yellow
Write-Host "   This may take 1-2 minutes..." -ForegroundColor Gray

try {
    $result = az cognitiveservices account deployment create `
        --name $resourceName `
        --resource-group $resourceGroup `
        --deployment-name $deploymentName `
        --model-name $modelName `
        --model-version $modelVersion `
        --model-format $modelFormat `
        --sku-capacity $skuCapacity `
        --sku-name $skuName `
        --output json 2>&1
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "   ✓ Deployment created successfully!" -ForegroundColor Green
        
        # Parse and display result
        try {
            $deployment = $result | ConvertFrom-Json
            Write-Host "`n   Deployment Details:" -ForegroundColor Cyan
            Write-Host "     Name: $($deployment.name)" -ForegroundColor White
            Write-Host "     Model: $($deployment.properties.model.name)" -ForegroundColor White
            Write-Host "     Version: $($deployment.properties.model.version)" -ForegroundColor White
            Write-Host "     Status: $($deployment.properties.provisioningState)" -ForegroundColor White
        } catch {
            # If parsing fails, just continue
        }
    } else {
        Write-Host "   ✗ Deployment failed!" -ForegroundColor Red
        Write-Host "   Error: $result" -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "   ✗ Deployment failed!" -ForegroundColor Red
    Write-Host "   Error: $_" -ForegroundColor Red
    exit 1
}

# Verify deployment
Write-Host "`n5. Verifying deployment..." -ForegroundColor Yellow
Start-Sleep -Seconds 5  # Wait a bit for deployment to be ready

try {
    $deployments = az cognitiveservices account deployment list `
        --name $resourceName `
        --resource-group $resourceGroup `
        --output json | ConvertFrom-Json
    
    $deployed = $deployments | Where-Object { $_.name -eq $deploymentName }
    
    if ($deployed) {
        Write-Host "   ✓ Deployment verified!" -ForegroundColor Green
    } else {
        Write-Host "   ⚠ Deployment created but not found in list yet" -ForegroundColor Yellow
        Write-Host "   (This is normal, it may take a moment to appear)" -ForegroundColor Gray
    }
} catch {
    Write-Host "   ⚠ Could not verify deployment" -ForegroundColor Yellow
}

Write-Host "`n============================================================" -ForegroundColor Green
Write-Host "✓ SUCCESS - Model Deployed!" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host "`nDeployment Name: $deploymentName" -ForegroundColor Cyan
Write-Host "`nNext Steps:" -ForegroundColor Yellow
Write-Host "  1. Run: python list_azure_deployments.py" -ForegroundColor White
Write-Host "  2. Then run: python test_integration.py" -ForegroundColor White
Write-Host "  3. Or use CLI: python -m cli.main" -ForegroundColor White
Write-Host "`n============================================================" -ForegroundColor Cyan
