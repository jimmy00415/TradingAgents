"""
Diagnostic script to show actual runtime configuration and vendor mappings
"""
import os

# Set environment like Streamlit does
if os.getenv("DISABLE_LOCAL_SOURCES") is None:
    os.environ["DISABLE_LOCAL_SOURCES"] = "true"
    print("✅ Set DISABLE_LOCAL_SOURCES=true")

from tradingagents.dataflows.interface import VENDOR_METHODS, get_vendor, get_category_for_method
from tradingagents.dataflows.config import get_config

def show_config():
    print("\n" + "="*70)
    print("CURRENT CONFIGURATION")
    print("="*70)
    
    config = get_config()
    
    print("\n📦 Category-level vendors (data_vendors):")
    for cat, vendor in config.get("data_vendors", {}).items():
        print(f"  {cat}: {vendor}")
    
    print("\n🔧 Tool-level vendors (tool_vendors):")
    for tool, vendor in config.get("tool_vendors", {}).items():
        print(f"  {tool}: {vendor}")
    
    print("\n🌍 Environment:")
    print(f"  DISABLE_LOCAL_SOURCES: {os.getenv('DISABLE_LOCAL_SOURCES')}")

def show_vendor_mappings():
    print("\n" + "="*70)
    print("VENDOR METHOD MAPPINGS (what's actually registered)")
    print("="*70)
    
    # Focus on problematic methods
    key_methods = ["get_news", "get_global_news"]
    
    for method in key_methods:
        if method in VENDOR_METHODS:
            vendors = list(VENDOR_METHODS[method].keys())
            print(f"\n📍 {method}:")
            print(f"   Registered vendors: {vendors}")
            
            # Show what config says
            try:
                category = get_category_for_method(method)
                vendor_config = get_vendor(category, method)
                print(f"   Config says: {vendor_config}")
            except Exception as e:
                print(f"   Config error: {e}")
        else:
            print(f"\n❌ {method}: NOT REGISTERED")

def test_vendor_resolution():
    print("\n" + "="*70)
    print("VENDOR RESOLUTION TEST (what will actually be called)")
    print("="*70)
    
    from tradingagents.dataflows.interface import route_to_vendor
    
    test_cases = [
        ("get_news", ["TSLA", "2026-01-01", "2026-01-14"]),
        ("get_global_news", ["2026-01-14", 7, 5]),
    ]
    
    for method, args in test_cases:
        print(f"\n🧪 Testing: {method}{tuple(args)}")
        try:
            # This will print debug info about vendor selection
            result = route_to_vendor(method, *args)
            if result:
                print(f"   ✅ Got result: {len(result)} chars")
            else:
                print(f"   ⚠️ Empty result")
        except Exception as e:
            print(f"   ❌ Error: {e}")
            import traceback
            traceback.print_exc()

def check_reddit_functions():
    print("\n" + "="*70)
    print("REDDIT FUNCTION CHECK (will they execute?)")
    print("="*70)
    
    from tradingagents.dataflows.local import get_reddit_global_news, get_reddit_company_news
    
    print("\n🧪 Calling get_reddit_global_news...")
    result1 = get_reddit_global_news("2026-01-14", 7, 5)
    print(f"   Result length: {len(result1)} (should be 0 if disabled)")
    
    print("\n🧪 Calling get_reddit_company_news...")
    result2 = get_reddit_company_news("TSLA", "2026-01-07", "2026-01-14")
    print(f"   Result length: {len(result2)} (should be 0 if disabled)")

if __name__ == "__main__":
    print("🔍 TradingAgents Configuration Diagnostics")
    print(f"Running at: {os.getcwd()}")
    
    show_config()
    show_vendor_mappings()
    check_reddit_functions()
    test_vendor_resolution()
    
    print("\n" + "="*70)
    print("DIAGNOSTIC COMPLETE")
    print("="*70)
    print("\n💡 Key things to check:")
    print("  1. tool_vendors should show 'get_news: finnhub,google'")
    print("  2. tool_vendors should show 'get_global_news: google'")
    print("  3. DISABLE_LOCAL_SOURCES should be 'true'")
    print("  4. Reddit functions should return 0 chars")
    print("  5. 'local' should NOT appear in actual execution")
