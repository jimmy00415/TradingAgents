"""Test Azure OpenAI function calling with bind_tools (simulating analyst behavior)"""
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
import os
from dotenv import load_dotenv

load_dotenv()

# Define a mock tool similar to what analysts use
@tool
def get_stock_data(ticker: str, start_date: str, end_date: str) -> str:
    """Get historical stock price data for a ticker."""
    return f"Mock stock data for {ticker} from {start_date} to {end_date}"

@tool
def get_news(ticker: str) -> str:
    """Get recent news for a ticker."""
    return f"Mock news for {ticker}"

def test_api_version(api_version: str):
    """Test if API version supports function calling (bind_tools)"""
    print(f"\n{'='*80}")
    print(f"Testing API Version: {api_version}")
    print('='*80)
    
    try:
        llm = AzureChatOpenAI(
            azure_deployment='gpt-4o-mini',
            azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT'),
            api_key=os.getenv('AZURE_OPENAI_API_KEY'),
            openai_api_version=api_version,
        )
        
        # Simulate what analysts do: bind tools
        tools = [get_stock_data, get_news]
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a stock analyst. Use tools to gather data."),
            ("user", "{input}")
        ])
        
        chain = prompt | llm.bind_tools(tools)
        
        # Test invocation
        response = chain.invoke({"input": "Get stock data for AAPL from 2024-01-01 to 2024-01-31"})
        
        print(f"✅ SUCCESS with API version {api_version}")
        print(f"   Response type: {type(response).__name__}")
        print(f"   Has tool_calls: {hasattr(response, 'tool_calls')}")
        if hasattr(response, 'tool_calls') and response.tool_calls:
            print(f"   Tool calls requested: {len(response.tool_calls)}")
            for tc in response.tool_calls:
                print(f"      - {tc.get('name', 'unknown')}")
        return True
        
    except Exception as e:
        print(f"❌ FAILED with API version {api_version}")
        print(f"   Error type: {type(e).__name__}")
        print(f"   Error message: {str(e)[:200]}")
        if "404" in str(e):
            print("   ⚠️  This is the 404 error causing analysis failures!")
        return False

if __name__ == "__main__":
    print("\n" + "="*80)
    print("AZURE OPENAI FUNCTION CALLING TEST")
    print("Testing which API version supports bind_tools (used by all analysts)")
    print("="*80)
    
    # Test different API versions
    versions_to_test = [
        "2024-10-21",      # Current version (causing issues?)
        "2024-08-01-preview",  # Recommended stable version
        "2024-06-01",      # Older stable version
        "2024-05-01-preview",  # Another preview version
    ]
    
    results = {}
    for version in versions_to_test:
        results[version] = test_api_version(version)
    
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    for version, success in results.items():
        status = "✅ WORKS" if success else "❌ FAILS (likely 404)"
        print(f"{version:25s} {status}")
    
    print("\n" + "="*80)
    print("RECOMMENDATION")
    print("="*80)
    working_versions = [v for v, success in results.items() if success]
    if working_versions:
        print(f"✅ Use API version: {working_versions[0]}")
        print(f"   Update AZURE_API_VERSION environment variable to: {working_versions[0]}")
    else:
        print("❌ No working API version found - check Azure OpenAI configuration")
