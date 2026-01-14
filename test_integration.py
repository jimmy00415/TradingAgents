"""
Quick integration test for TradingAgents
Runs a minimal analysis on a single ticker with minimal configuration
"""

from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG
from dotenv import load_dotenv
import datetime

# Load environment variables
load_dotenv()

print("=" * 60)
print("TradingAgents Integration Test")
print("=" * 60)

# Create a minimal config for faster testing
config = DEFAULT_CONFIG.copy()
# Use default gpt-4o deployment (should exist in Azure)
config["deep_think_llm"] = "gpt-4o"
config["quick_think_llm"] = "gpt-4o"
config["max_debate_rounds"] = 1  # Minimal rounds for testing

# Configure data vendors
config["data_vendors"] = {
    "core_stock_apis": "yfinance",           # Free, no API key needed
    "technical_indicators": "yfinance",      # Free, no API key needed
    "fundamental_data": "alpha_vantage",     # Requires API key
    "news_data": "alpha_vantage",            # Requires API key
}

print("\nConfiguration:")
print(f"  Ticker: AAPL")
print(f"  Date: 2024-05-10")
print(f"  Deep Think LLM: {config['deep_think_llm']}")
print(f"  Quick Think LLM: {config['quick_think_llm']}")
print(f"  Max Debate Rounds: {config['max_debate_rounds']}")

try:
    # Initialize TradingAgentsGraph
    print("\nInitializing TradingAgentsGraph...")
    ta = TradingAgentsGraph(debug=True, config=config)
    print("✓ TradingAgentsGraph initialized")
    
    # Run propagation (analysis)
    print("\nRunning analysis on AAPL for 2024-05-10...")
    print("(This will take a few minutes as it fetches data and runs LLM agents)")
    print("-" * 60)
    
    state, decision = ta.propagate("AAPL", "2024-05-10")
    
    print("-" * 60)
    print("\n✓ Analysis completed successfully!")
    print("\n" + "=" * 60)
    print("FINAL DECISION")
    print("=" * 60)
    print(decision)
    print("=" * 60)
    
    # Check if results were saved
    import os
    result_dir = f"results/AAPL/2024-05-10"
    if os.path.exists(result_dir):
        print(f"\n✓ Results saved to: {result_dir}")
        if os.path.exists(f"{result_dir}/reports"):
            print(f"✓ Reports directory created")
    
    print("\n" + "=" * 60)
    print("✓ Integration test PASSED!")
    print("=" * 60)
    print("\nThe TradingAgents system is working correctly!")
    print("You can now:")
    print("  1. Run full analyses with main.py")
    print("  2. Use the interactive CLI with: python -m cli.main")
    print("  3. Launch the Streamlit app: streamlit run streamlit_app.py")
    
except KeyboardInterrupt:
    print("\n\n⚠ Test interrupted by user")
    print("The system appears to be working (it started the analysis)")
    
except Exception as e:
    print(f"\n✗ Test failed with error: {e}")
    import traceback
    traceback.print_exc()
    print("\nPlease check:")
    print("  1. API keys are configured in .env")
    print("  2. You have internet connectivity")
    print("  3. API services are accessible")
