# Quick Upgrade to 10K tokens/min (10x current limit)

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Quick Deployment Upgrade: 1K → 10K tokens/min" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan

$resourceName = "Jimmy00415"
$resourceGroup = "TradingAgent"
$deploymentName = "gpt-4o"
$newCapacity = "10"

Write-Host "`nThis will:" -ForegroundColor Yellow
Write-Host "  ✓ Increase rate limit: 1K → 10K tokens/min (10x faster!)" -ForegroundColor Green
Write-Host "  ✓ Keep same deployment name: $deploymentName" -ForegroundColor Green
Write-Host "  ✓ Same pay-per-token pricing" -ForegroundColor Green
Write-Host "`n  ⚠ Requires: Delete and recreate deployment (1-2 min downtime)" -ForegroundColor Yellow

$confirm = Read-Host "`nProceed with upgrade? (y/N)"

if ($confirm -ne 'y' -and $confirm -ne 'Y') {
    Write-Host "`nUpgrade cancelled." -ForegroundColor Yellow
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
    Write-Host "   ✗ Failed" -ForegroundColor Red
    exit 1
}

Write-Host "`n2. Creating upgraded deployment (10K tokens/min)..." -ForegroundColor Yellow
Write-Host "   Please wait 1-2 minutes..." -ForegroundColor Gray

$result = az cognitiveservices account deployment create `
    --name $resourceName `
    --resource-group $resourceGroup `
    --deployment-name $deploymentName `
    --model-name gpt-4o `
    --model-version "2024-11-20" `
    --model-format OpenAI `
    --sku-capacity $newCapacity `
    --sku-name "Standard" `
    --output json 2>&1

if ($LASTEXITCODE -eq 0) {
    Write-Host "   ✓ Success!" -ForegroundColor Green
    
    $deployment = $result | ConvertFrom-Json
    Write-Host "`n============================================================" -ForegroundColor Green
    Write-Host "✓ Upgrade Complete!" -ForegroundColor Green
    Write-Host "============================================================" -ForegroundColor Green
    Write-Host "`nNew Configuration:" -ForegroundColor Cyan
    Write-Host "  Deployment: $($deployment.name)" -ForegroundColor White
    Write-Host "  Capacity: 10,000 tokens/min (was 1,000)" -ForegroundColor Green
    Write-Host "  That's 10x faster!" -ForegroundColor Green
    
    Write-Host "`nYou can now:" -ForegroundColor Yellow
    Write-Host "  ✓ Run analyses without waiting 60 seconds" -ForegroundColor White
    Write-Host "  ✓ Handle multiple concurrent requests" -ForegroundColor White
    Write-Host "  ✓ Process complex analyses faster" -ForegroundColor White
    
    Write-Host "`nTest it now:" -ForegroundColor Cyan
    Write-Host "  Refresh: http://localhost:8502" -ForegroundColor White
    
} else {
    Write-Host "   ✗ Failed!" -ForegroundColor Red
    Write-Host "   Error: $result" -ForegroundColor Red
    exit 1
}

Write-Host "`n============================================================" -ForegroundColor Cyan
