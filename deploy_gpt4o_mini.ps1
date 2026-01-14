# Deploy gpt-4o-mini for Economy Mode
# This model is 70% cheaper and perfect for research/analysis tasks

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Deploy gpt-4o-mini for Economy Mode" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan

$resourceName = "Jimmy00415"
$resourceGroup = "TradingAgent"
$deploymentName = "gpt-4o-mini"
$modelName = "gpt-4o-mini"
$modelVersion = "2024-07-18"
$capacity = "50"  # Higher capacity since it's cheaper

Write-Host "`nBenefits:" -ForegroundColor Yellow
Write-Host "  ✓ 70% cheaper than gpt-4o" -ForegroundColor Green
Write-Host "  ✓ Faster responses" -ForegroundColor Green
Write-Host "  ✓ Higher capacity (50K tokens/min)" -ForegroundColor Green
Write-Host "  ✓ Perfect for data gathering & initial analysis" -ForegroundColor Green

Write-Host "`nThis deployment will:" -ForegroundColor Yellow
Write-Host "  • Deploy gpt-4o-mini with 50K tokens/min capacity" -ForegroundColor White
Write-Host "  • Enable economy mode automatically" -ForegroundColor White
Write-Host "  • Reduce costs by ~70%" -ForegroundColor White
Write-Host "  • Maintain quality (gpt-4o used for final decisions)" -ForegroundColor White

$confirm = Read-Host "`nDeploy gpt-4o-mini? (y/N)"

if ($confirm -ne 'y' -and $confirm -ne 'Y') {
    Write-Host "`nDeployment cancelled." -ForegroundColor Yellow
    exit 0
}

Write-Host "`nDeploying gpt-4o-mini (capacity: 50K tokens/min)..." -ForegroundColor Yellow
Write-Host "Please wait 1-2 minutes..." -ForegroundColor Gray

$result = az cognitiveservices account deployment create `
    --name $resourceName `
    --resource-group $resourceGroup `
    --deployment-name $deploymentName `
    --model-name $modelName `
    --model-version $modelVersion `
    --model-format OpenAI `
    --sku-capacity $capacity `
    --sku-name "Standard" `
    --output json 2>&1

if ($LASTEXITCODE -eq 0) {
    $deployment = $result | ConvertFrom-Json
    Write-Host "`n============================================================" -ForegroundColor Green
    Write-Host "✓ Deployment Complete!" -ForegroundColor Green
    Write-Host "============================================================" -ForegroundColor Green
    Write-Host "`nDeployment Details:" -ForegroundColor Cyan
    Write-Host "  Name: $($deployment.name)" -ForegroundColor White
    Write-Host "  Model: $modelName" -ForegroundColor White
    Write-Host "  Capacity: 50,000 tokens/min" -ForegroundColor Green
    Write-Host "  Cost: ~70% less than gpt-4o" -ForegroundColor Green
    
    Write-Host "`nEconomy Mode Status:" -ForegroundColor Cyan
    Write-Host "  ✓ Researchers: gpt-4o-mini (fast & cheap)" -ForegroundColor White
    Write-Host "  ✓ Analysts: gpt-4o-mini (good quality)" -ForegroundColor White
    Write-Host "  ✓ Final Decision: gpt-4o (high quality)" -ForegroundColor White
    
    Write-Host "`nYour Deployments:" -ForegroundColor Yellow
    az cognitiveservices account deployment list `
        --name $resourceName `
        --resource-group $resourceGroup `
        --query "[].{name:name, model:properties.model.name, capacity:sku.capacity}" `
        -o table
    
    Write-Host "`nNext Steps:" -ForegroundColor Cyan
    Write-Host "  1. Economy mode is now ENABLED by default" -ForegroundColor White
    Write-Host "  2. Restart Streamlit to use new configuration" -ForegroundColor White
    Write-Host "  3. Run analysis - should complete without rate limits!" -ForegroundColor White
    
} else {
    Write-Host "`n✗ Deployment Failed!" -ForegroundColor Red
    Write-Host "Error: $result" -ForegroundColor Red
    
    Write-Host "`nTroubleshooting:" -ForegroundColor Yellow
    Write-Host "  • Check if model version is supported in your region" -ForegroundColor White
    Write-Host "  • Verify Azure quota availability" -ForegroundColor White
    Write-Host "  • Try: az cognitiveservices account list-models -n $resourceName -g $resourceGroup" -ForegroundColor White
    exit 1
}

Write-Host "`n============================================================" -ForegroundColor Cyan
