# Quick Deployment Script for Streamlit Cloud

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Streamlit Cloud Deployment Preparation" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan

Write-Host "`n1. Checking git status..." -ForegroundColor Yellow
$gitStatus = git status --porcelain
if ($gitStatus) {
    Write-Host "   Found uncommitted changes:" -ForegroundColor Yellow
    git status --short
    
    Write-Host "`n2. Committing changes..." -ForegroundColor Yellow
    git add .
    git commit -m "Configure for Streamlit Cloud deployment with Azure OpenAI API v2024-10-21"
    
    Write-Host "`n3. Pushing to GitHub..." -ForegroundColor Yellow
    git push origin main
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "   ✓ Pushed successfully!" -ForegroundColor Green
    } else {
        Write-Host "   ✗ Push failed!" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "   ✓ No uncommitted changes" -ForegroundColor Green
}

Write-Host "`n============================================================" -ForegroundColor Green
Write-Host "✓ Ready for Streamlit Cloud Deployment!" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green

Write-Host "`nNext Steps:" -ForegroundColor Yellow
Write-Host "  1. Go to: https://share.streamlit.io" -ForegroundColor White
Write-Host "  2. Click 'New app'" -ForegroundColor White
Write-Host "  3. Select repository: TauricResearch/TradingAgents" -ForegroundColor White
Write-Host "  4. Branch: main" -ForegroundColor White
Write-Host "  5. Main file: streamlit_app.py" -ForegroundColor White
Write-Host "  6. Click 'Advanced settings' → 'Secrets'" -ForegroundColor White
Write-Host "  7. Paste secrets (see STREAMLIT_CLOUD_DEPLOYMENT.md)" -ForegroundColor White
Write-Host "  8. Click 'Deploy'!" -ForegroundColor White

Write-Host "`nLocal testing:" -ForegroundColor Yellow
Write-Host "  App is running at: http://localhost:8502" -ForegroundColor Cyan

Write-Host "`nFor detailed instructions, see:" -ForegroundColor Yellow
Write-Host "  STREAMLIT_CLOUD_DEPLOYMENT.md" -ForegroundColor Cyan

Write-Host "`n============================================================" -ForegroundColor Cyan
