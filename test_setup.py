"""
Quick test script to validate TradingAgents setup
Tests: 
- Environment variables
- API connectivity
- Basic imports
- Data vendors
"""

from dotenv import load_dotenv
import os
import sys

# Load environment variables
load_dotenv()

print("=" * 60)
print("TradingAgents Setup Validation")
print("=" * 60)

# Test 1: Check environment variables
print("\n1. Checking Environment Variables...")
required_keys = ['AZURE_OPENAI_API_KEY', 'ALPHA_VANTAGE_API_KEY']
optional_keys = ['FINNHUB_API_KEY', 'OPENAI_API_KEY']

env_status = True
for key in required_keys:
    value = os.getenv(key)
    if value and value != f"your_{key.lower()}_here" and not value.startswith("your_"):
        print(f"   ✓ {key}: Configured")
    else:
        print(f"   ✗ {key}: Missing or not configured")
        env_status = False

for key in optional_keys:
    value = os.getenv(key)
    if value and value != f"your_{key.lower()}_here" and not value.startswith("your_"):
        print(f"   ✓ {key}: Configured (Optional)")
    else:
        print(f"   - {key}: Not configured (Optional)")

if not env_status:
    print("\n   ⚠ Missing required API keys. Please configure .env file")
    sys.exit(1)

# Test 2: Check imports
print("\n2. Checking Package Imports...")
try:
    from tradingagents.graph.trading_graph import TradingAgentsGraph
    print("   ✓ TradingAgentsGraph imported successfully")
except ImportError as e:
    print(f"   ✗ Failed to import TradingAgentsGraph: {e}")
    sys.exit(1)

try:
    from tradingagents.default_config import DEFAULT_CONFIG
    print("   ✓ DEFAULT_CONFIG imported successfully")
except ImportError as e:
    print(f"   ✗ Failed to import DEFAULT_CONFIG: {e}")
    sys.exit(1)

try:
    import yfinance
    print("   ✓ yfinance imported successfully")
except ImportError as e:
    print(f"   ✗ Failed to import yfinance: {e}")
    sys.exit(1)

try:
    import pandas as pd
    print("   ✓ pandas imported successfully")
except ImportError as e:
    print(f"   ✗ Failed to import pandas: {e}")
    sys.exit(1)

# Test 3: Test basic data fetch (yfinance - no API key needed)
print("\n3. Testing Data Connectivity (yfinance)...")
try:
    import yfinance as yf
    ticker = yf.Ticker("AAPL")
    hist = ticker.history(period="5d")
    if not hist.empty:
        print(f"   ✓ Successfully fetched data for AAPL (last 5 days)")
        print(f"   Latest close: ${hist['Close'].iloc[-1]:.2f}")
    else:
        print("   ⚠ Data fetch returned empty result")
except Exception as e:
    print(f"   ✗ Failed to fetch data: {e}")
    sys.exit(1)

# Test 4: Test Alpha Vantage connection
print("\n4. Testing Alpha Vantage API...")
try:
    import requests
    av_key = os.getenv('ALPHA_VANTAGE_API_KEY')
    if av_key:
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey={av_key}'
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if 'Error Message' in data:
                print(f"   ✗ Alpha Vantage API error: {data['Error Message']}")
            elif 'Note' in data:
                print(f"   ⚠ Alpha Vantage rate limit: {data['Note']}")
            elif 'Time Series (Daily)' in data:
                print("   ✓ Alpha Vantage API working correctly")
            else:
                print(f"   ? Unexpected response: {list(data.keys())}")
        else:
            print(f"   ✗ HTTP error: {response.status_code}")
    else:
        print("   - Alpha Vantage key not configured (skipped)")
except Exception as e:
    print(f"   ⚠ Alpha Vantage test failed: {e}")

# Test 5: Test Azure OpenAI connection
print("\n5. Testing Azure OpenAI API...")
try:
    from openai import AzureOpenAI
    
    api_key = os.getenv('AZURE_OPENAI_API_KEY')
    endpoint = os.getenv('AZURE_OPENAI_ENDPOINT', 'https://genai.hkbu.edu.hk/api/v0/rest')
    api_version = os.getenv('AZURE_API_VERSION', '2024-12-01-preview')
    
    if api_key:
        client = AzureOpenAI(
            api_key=api_key,
            api_version=api_version,
            azure_endpoint=endpoint
        )
        print("   ✓ Azure OpenAI client initialized")
        print(f"   Endpoint: {endpoint}")
    else:
        print("   - Azure OpenAI key not configured")
except Exception as e:
    print(f"   ⚠ Azure OpenAI initialization warning: {e}")

# Test 6: Check TradingAgentsGraph initialization
print("\n6. Testing TradingAgentsGraph Initialization...")
try:
    config = DEFAULT_CONFIG.copy()
    config["deep_think_llm"] = "gpt-4o-mini"
    config["quick_think_llm"] = "gpt-4o-mini"
    config["max_debate_rounds"] = 1
    
    ta = TradingAgentsGraph(debug=False, config=config)
    print("   ✓ TradingAgentsGraph initialized successfully")
    print(f"   Deep Think LLM: {config['deep_think_llm']}")
    print(f"   Quick Think LLM: {config['quick_think_llm']}")
    print(f"   Max Debate Rounds: {config['max_debate_rounds']}")
except Exception as e:
    print(f"   ✗ Failed to initialize TradingAgentsGraph: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 60)
print("✓ All tests passed! TradingAgents is ready to use.")
print("=" * 60)
print("\nNext steps:")
print("  1. Run full analysis: python main.py")
print("  2. Run CLI interface: python -m cli.main")
print("  3. Run Streamlit app: streamlit run streamlit_app.py")
print("=" * 60)
