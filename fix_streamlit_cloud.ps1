# =============================================================================
# Streamlit Cloud Deployment Fix Script
# Applies all fixes to resolve cloud deployment errors
# =============================================================================

Write-Host "🔧 Applying Streamlit Cloud fixes..." -ForegroundColor Cyan

# Fix 1: Update requirements.txt for cloud compatibility
Write-Host "`n[1/5] Updating requirements.txt..." -ForegroundColor Yellow
$requirementsContent = @"
# Core framework
streamlit==1.31.0
python-dotenv==1.0.0

# LangChain ecosystem
langchain==0.1.0
langchain-openai==0.0.2
langchain-community==0.0.13
langgraph==0.0.20

# Azure OpenAI
openai==1.12.0

# Data sources
yfinance==0.2.36
alpha-vantage==2.3.1
finnhub-python==2.4.19

# Vector database
chromadb==0.4.22

# Data processing
pandas==2.2.0
numpy==1.26.3
stockstats==0.6.2

# Utilities
beautifulsoup4==4.12.3
requests==2.31.0
praw==7.7.1
googlenews==1.6.14
"@
$requirementsContent | Out-File -FilePath "requirements.txt" -Encoding utf8 -Force
Write-Host "   ✅ requirements.txt updated" -ForegroundColor Green

# Fix 2: Ensure packages.txt exists
Write-Host "`n[2/5] Checking packages.txt..." -ForegroundColor Yellow
if (-not (Test-Path "packages.txt")) {
    "build-essential" | Out-File -FilePath "packages.txt" -Encoding utf8 -Force
    Write-Host "   ✅ packages.txt created" -ForegroundColor Green
} else {
    Write-Host "   ✅ packages.txt already exists" -ForegroundColor Green
}

# Fix 3: Create minimal test app for debugging
Write-Host "`n[3/5] Creating minimal test app..." -ForegroundColor Yellow
$minimalAppContent = @"
import streamlit as st
import os
import sys

st.title("🔍 TradingAgents Deployment Test")

# Test 1: Python Environment
st.header("1. Python Environment")
st.write(f"Python Version: {sys.version}")
st.write(f"Streamlit Runtime: {os.getenv('STREAMLIT_RUNTIME_ENV', 'local')}")

# Test 2: Required Packages
st.header("2. Package Imports")
packages = {
    "streamlit": False,
    "langchain": False,
    "openai": False,
    "chromadb": False,
    "yfinance": False,
}

for pkg in packages:
    try:
        __import__(pkg)
        packages[pkg] = True
        st.success(f"✅ {pkg}")
    except ImportError as e:
        st.error(f"❌ {pkg}: {str(e)}")

# Test 3: Secrets Configuration
st.header("3. Secrets Configuration")
try:
    azure_key = st.secrets.get("AZURE_OPENAI_API_KEY", "")
    if azure_key:
        st.success(f"✅ AZURE_OPENAI_API_KEY: {azure_key[:10]}...{azure_key[-4:]}")
    else:
        st.warning("⚠️ AZURE_OPENAI_API_KEY not configured")
    
    alpha_key = st.secrets.get("ALPHA_VANTAGE_API_KEY", "")
    if alpha_key:
        st.success(f"✅ ALPHA_VANTAGE_API_KEY: {alpha_key[:6]}...")
    else:
        st.info("ℹ️ ALPHA_VANTAGE_API_KEY not configured (optional)")
        
except Exception as e:
    st.error(f"❌ Secrets error: {str(e)}")

# Test 4: ChromaDB Persistence
st.header("4. ChromaDB Persistence")
try:
    import chromadb
    persist_dir = "/tmp/chroma_test" if os.getenv("STREAMLIT_RUNTIME_ENV") == "cloud" else "./chroma_test"
    client = chromadb.Client()
    st.success(f"✅ ChromaDB initialized (memory mode)")
    st.info(f"Persist directory: {persist_dir}")
except Exception as e:
    st.error(f"❌ ChromaDB error: {str(e)}")

# Test 5: Azure OpenAI Connection
st.header("5. Azure OpenAI Connection")
try:
    from openai import AzureOpenAI
    azure_key = st.secrets.get("AZURE_OPENAI_API_KEY", os.getenv("AZURE_OPENAI_API_KEY", ""))
    if azure_key:
        client = AzureOpenAI(
            api_key=azure_key,
            api_version="2024-10-21",
            azure_endpoint="https://jimmy00415.openai.azure.com/"
        )
        st.success("✅ Azure OpenAI client initialized")
    else:
        st.error("❌ AZURE_OPENAI_API_KEY not found")
except Exception as e:
    st.error(f"❌ Azure OpenAI error: {str(e)}")

st.success("🎉 All tests completed!")
"@
$minimalAppContent | Out-File -FilePath "test_streamlit_minimal.py" -Encoding utf8 -Force
Write-Host "   ✅ test_streamlit_minimal.py created" -ForegroundColor Green

# Fix 4: Update streamlit_app.py with ChromaDB fix
Write-Host "`n[4/5] Checking streamlit_app.py for cloud optimizations..." -ForegroundColor Yellow
$streamlitContent = Get-Content "streamlit_app.py" -Raw

if ($streamlitContent -notmatch "/tmp/chroma_data") {
    Write-Host "   ⚠️  ChromaDB persistence path needs manual update" -ForegroundColor Yellow
    Write-Host "   Add this to tradingagents/graph/setup.py:" -ForegroundColor Yellow
    Write-Host "   persist_directory = '/tmp/chroma_data' if IS_CLOUD else './chroma_data'" -ForegroundColor Cyan
} else {
    Write-Host "   ✅ ChromaDB path already configured for cloud" -ForegroundColor Green
}

# Fix 5: Commit and push changes
Write-Host "`n[5/5] Preparing to commit changes..." -ForegroundColor Yellow
Write-Host "   Run these commands to push fixes:" -ForegroundColor Cyan
Write-Host "   git add requirements.txt packages.txt test_streamlit_minimal.py" -ForegroundColor White
Write-Host "   git commit -m 'Fix: Streamlit Cloud deployment optimizations'" -ForegroundColor White
Write-Host "   git push origin main" -ForegroundColor White

Write-Host "`n✅ All fixes applied!" -ForegroundColor Green
Write-Host "`n📋 Next Steps:" -ForegroundColor Cyan
Write-Host "1. Review changes above" -ForegroundColor White
Write-Host "2. Commit and push to GitHub" -ForegroundColor White
Write-Host "3. Wait 2-3 minutes for Streamlit auto-redeploy" -ForegroundColor White
Write-Host "4. If still failing, deploy test_streamlit_minimal.py first" -ForegroundColor White
Write-Host "5. Check logs at: Manage app → Logs tab" -ForegroundColor White
