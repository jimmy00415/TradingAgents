import streamlit as st
import sys
import os

st.set_page_config(page_title="TradingAgents - Cloud Test", page_icon="🔍")
st.title("🔍 TradingAgents Cloud Deployment Diagnostic")

# Test 1: Environment
st.header("1. Environment Check")
st.write(f"**Python Version:** {sys.version}")
st.write(f"**Streamlit Runtime:** {os.getenv('STREAMLIT_RUNTIME_ENV', 'local')}")
st.success("✅ Environment OK")

# Test 2: Core Imports
st.header("2. Core Package Imports")
packages_to_test = [
    ("streamlit", "Streamlit"),
    ("langchain", "LangChain"),
    ("langchain_openai", "LangChain OpenAI"),
    ("langgraph", "LangGraph"),
    ("openai", "OpenAI SDK"),
    ("chromadb", "ChromaDB"),
    ("yfinance", "Yahoo Finance"),
    ("pandas", "Pandas"),
    ("numpy", "NumPy"),
]

all_ok = True
for pkg, name in packages_to_test:
    try:
        __import__(pkg)
        st.success(f"✅ {name}")
    except ImportError as e:
        st.error(f"❌ {name}: {str(e)}")
        all_ok = False

if all_ok:
    st.success("✅ All core packages imported successfully!")

# Test 3: Secrets Configuration  
st.header("3. Secrets Configuration")
try:
    azure_key = st.secrets.get("AZURE_OPENAI_API_KEY", "")
    if azure_key:
        masked_key = f"{azure_key[:10]}...{azure_key[-4:]}" if len(azure_key) > 14 else "***"
        st.success(f"✅ AZURE_OPENAI_API_KEY: {masked_key}")
    else:
        st.error("❌ AZURE_OPENAI_API_KEY not configured")
    
    alpha_key = st.secrets.get("ALPHA_VANTAGE_API_KEY", "")
    if alpha_key:
        st.success(f"✅ ALPHA_VANTAGE_API_KEY: {alpha_key[:6]}...")
    else:
        st.warning("⚠️ ALPHA_VANTAGE_API_KEY not configured (optional)")
        
except Exception as e:
    st.error(f"❌ Secrets error: {str(e)}")

# Test 4: ChromaDB Initialization
st.header("4. ChromaDB Test")
try:
    import chromadb
    from chromadb.config import Settings
    
    client = chromadb.Client(Settings(allow_reset=True))
    collection = client.create_collection("test_collection")
    st.success("✅ ChromaDB initialized (in-memory mode)")
    
    # Clean up
    client.delete_collection("test_collection")
except Exception as e:
    st.error(f"❌ ChromaDB error: {str(e)}")
    import traceback
    st.code(traceback.format_exc())

# Test 5: Azure OpenAI Connection
st.header("5. Azure OpenAI Connection Test")
try:
    from openai import AzureOpenAI
    
    azure_key = st.secrets.get("AZURE_OPENAI_API_KEY", os.getenv("AZURE_OPENAI_API_KEY", ""))
    azure_endpoint = st.secrets.get("AZURE_OPENAI_ENDPOINT", "https://jimmy00415.openai.azure.com/")
    azure_version = st.secrets.get("AZURE_API_VERSION", "2024-10-21")
    
    if azure_key:
        client = AzureOpenAI(
            api_key=azure_key,
            api_version=azure_version,
            azure_endpoint=azure_endpoint
        )
        st.success("✅ Azure OpenAI client initialized")
        st.info(f"Endpoint: {azure_endpoint}")
        st.info(f"API Version: {azure_version}")
    else:
        st.error("❌ AZURE_OPENAI_API_KEY not found in secrets")
except Exception as e:
    st.error(f"❌ Azure OpenAI error: {str(e)}")
    import traceback
    st.code(traceback.format_exc())

# Test 6: TradingAgents Import
st.header("6. TradingAgents Module Test")
try:
    from tradingagents.graph.trading_graph import TradingAgentsGraph
    from tradingagents.default_config import DEFAULT_CONFIG
    st.success("✅ TradingAgents modules imported")
    st.info(f"Economy Mode: {'ON' if DEFAULT_CONFIG.get('economy_mode', True) else 'OFF'}")
except Exception as e:
    st.error(f"❌ TradingAgents import error: {str(e)}")
    import traceback
    st.code(traceback.format_exc())

# Final Summary
st.header("📊 Diagnostic Summary")
if all_ok:
    st.success("🎉 **All tests passed!** Your deployment should work.")
    st.info("Switch Main file path back to `streamlit_app.py` in Streamlit Cloud settings.")
else:
    st.error("⚠️ **Some tests failed.** Check the errors above and fix them.")
    st.info("Common fixes:")
    st.markdown("""
    - Missing packages: Check requirements.txt
    - Secrets not configured: Add them in Streamlit Cloud Settings → Secrets
    - ChromaDB issues: Make sure packages.txt has `build-essential`
    """)
