# Upgrade Azure OpenAI Deployment for Higher Rate Limits
# This will increase your quota from 1K tokens/min to higher limits

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Azure OpenAI Deployment Upgrade" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan

$resourceName = "Jimmy00415"
$resourceGroup = "TradingAgent"
$deploymentName = "gpt-4o"

Write-Host "`nCurrent Configuration:" -ForegroundColor Yellow
Write-Host "  Resource: $resourceName"
Write-Host "  Deployment: $deploymentName"
Write-Host "  Current Tier: S0 (1K tokens/min, 1 req/10sec)"

Write-Host "`n============================================================" -ForegroundColor Yellow
Write-Host "Upgrade Options:" -ForegroundColor Yellow
Write-Host "============================================================" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Standard Deployment (Recommended)" -ForegroundColor Green
Write-Host "   - Capacity: 10-50K tokens/min"
Write-Host "   - SKU Capacity: 10-50"
Write-Host "   - Cost: Pay-per-token"
Write-Host ""
Write-Host "2. PTU (Provisioned Throughput)" -ForegroundColor Cyan
Write-Host "   - Capacity: Reserved, no rate limits"
Write-Host "   - Cost: Monthly fixed cost"
Write-Host "   - Best for: Production with consistent usage"
Write-Host ""

$choice = Read-Host "Choose upgrade option (1 or 2, or 'c' to cancel)"

if ($choice -eq 'c' -or $choice -eq 'C') {
    Write-Host "`nUpgrade cancelled." -ForegroundColor Yellow
    exit 0
}

if ($choice -eq '1') {
    # Standard deployment upgrade
    Write-Host "`n============================================================" -ForegroundColor Green
    Write-Host "Upgrading to Standard with Higher Capacity" -ForegroundColor Green
    Write-Host "============================================================" -ForegroundColor Green
    
    $capacity = Read-Host "`nEnter desired capacity (10-50 recommended, press Enter for 10)"
    if ([string]::IsNullOrWhiteSpace($capacity)) {
        $capacity = "10"
    }
    
    Write-Host "`nUpgrading deployment with capacity: $capacity K tokens/min" -ForegroundColor Cyan
    Write-Host "This will:"
    Write-Host "  - Delete the existing deployment"
    Write-Host "  - Create a new deployment with higher capacity"
    Write-Host "  - Keep the same deployment name: $deploymentName"
    
    $confirm = Read-Host "`nContinue? (y/N)"
    if ($confirm -ne 'y' -and $confirm -ne 'Y') {
        Write-Host "Upgrade cancelled." -ForegroundColor Yellow
        exit 0
    }
    
    Write-Host "`n1. Deleting existing deployment..." -ForegroundColor Yellow
    az cognitiveservices account deployment delete `
        --name $resourceName `
        --resource-group $resourceGroup `
        --deployment-name $deploymentName `
        --output none
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "   ✓ Deleted" -ForegroundColor Green
    } else {
        Write-Host "   ✗ Failed to delete" -ForegroundColor Red
        exit 1
    }
    
    Write-Host "`n2. Creating upgraded deployment..." -ForegroundColor Yellow
    Write-Host "   (This takes 1-2 minutes...)" -ForegroundColor Gray
    
    $result = az cognitiveservices account deployment create `
        --name $resourceName `
        --resource-group $resourceGroup `
        --deployment-name $deploymentName `
        --model-name gpt-4o `
        --model-version "2024-11-20" `
        --model-format OpenAI `
        --sku-capacity $capacity `
        --sku-name "Standard" `
        --output json 2>&1
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "   ✓ Deployment upgraded!" -ForegroundColor Green
        
        $deployment = $result | ConvertFrom-Json
        Write-Host "`n   New Configuration:" -ForegroundColor Cyan
        Write-Host "     Deployment: $($deployment.name)" -ForegroundColor White
        Write-Host "     Capacity: $capacity K tokens/min" -ForegroundColor White
        Write-Host "     Status: $($deployment.properties.provisioningState)" -ForegroundColor White
    } else {
        Write-Host "   ✗ Deployment failed!" -ForegroundColor Red
        Write-Host "   Error: $result" -ForegroundColor Red
        exit 1
    }
    
} elseif ($choice -eq '2') {
    Write-Host "`n============================================================" -ForegroundColor Cyan
    Write-Host "PTU (Provisioned Throughput) Deployment" -ForegroundColor Cyan
    Write-Host "============================================================" -ForegroundColor Cyan
    
    Write-Host "`nPTU deployments require:" -ForegroundColor Yellow
    Write-Host "  - Azure quota approval"
    Write-Host "  - Commitment to reserved capacity"
    Write-Host "  - Monthly fixed cost"
    
    Write-Host "`nTo request PTU:" -ForegroundColor Cyan
    Write-Host "  1. Visit: https://aka.ms/oai/quotaincrease"
    Write-Host "  2. Select 'Provisioned' deployment type"
    Write-Host "  3. Specify required PTU units"
    Write-Host "  4. Wait for approval (can take 1-3 business days)"
    
    Write-Host "`nAfter approval, you can create PTU deployment via Azure Portal." -ForegroundColor Green
    exit 0
    
} else {
    Write-Host "`nInvalid choice. Upgrade cancelled." -ForegroundColor Red
    exit 1
}

Write-Host "`n============================================================" -ForegroundColor Green
Write-Host "✓ Upgrade Complete!" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green

Write-Host "`nNew Rate Limits:" -ForegroundColor Cyan
Write-Host "  - Tokens: $capacity K per minute" -ForegroundColor White
Write-Host "  - Much higher than previous 1K/min!" -ForegroundColor Green

Write-Host "`nTest your upgraded deployment:" -ForegroundColor Yellow
Write-Host "  1. Wait 30 seconds for deployment to be ready"
Write-Host "  2. Refresh Streamlit app: http://localhost:8502"
Write-Host "  3. Try running an analysis again"

Write-Host "`n============================================================" -ForegroundColor Cyan
