"""
Test script to verify yfinance get_fundamentals implementation
"""
from tradingagents.dataflows.y_finance import get_fundamentals
from tradingagents.dataflows.interface import VENDOR_METHODS
from tradingagents.default_config import DEFAULT_CONFIG

def test_direct_yfinance():
    """Test direct call to yfinance get_fundamentals"""
    print("=" * 80)
    print("TEST 1: Direct yfinance get_fundamentals call")
    print("=" * 80)
    
    try:
        result = get_fundamentals("TSLA", "2026-01-14")
        print(result[:500])  # Print first 500 chars
        print("...")
        print(f"\nTotal length: {len(result)} characters")
        
        success = len(result) > 100 and "TSLA" in result and "404" not in result
        print("✅ Direct call PASSED" if success else "❌ Direct call FAILED")
        return success
    except Exception as e:
        print(f"❌ Direct call FAILED with exception: {e}")
        return False

def test_vendor_mapping():
    """Test that vendor mapping is correct"""
    print("\n" + "=" * 80)
    print("TEST 2: Vendor mapping verification")
    print("=" * 80)
    
    fundamentals_vendors = VENDOR_METHODS.get("get_fundamentals", {})
    print(f"Available vendors for get_fundamentals: {list(fundamentals_vendors.keys())}")
    
    has_yfinance = "yfinance" in fundamentals_vendors
    print(f"✅ yfinance IS mapped" if has_yfinance else "❌ yfinance NOT mapped")
    
    if has_yfinance:
        func = fundamentals_vendors["yfinance"]
        print(f"Mapped function: {func.__name__} from {func.__module__}")
    
    return has_yfinance

def test_config():
    """Test that config uses yfinance"""
    print("\n" + "=" * 80)
    print("TEST 3: Configuration check")
    print("=" * 80)
    
    vendor = DEFAULT_CONFIG['data_vendors']['fundamental_data']
    print(f"Config fundamental_data vendor: {vendor}")
    
    success = vendor == "yfinance"
    print(f"✅ Config correct" if success else f"❌ Config set to '{vendor}' instead of 'yfinance'")
    return success

def main():
    print("\n🔍 YFINANCE GET_FUNDAMENTALS FIX VERIFICATION")
    print("=" * 80)
    
    results = []
    
    # Run all tests
    results.append(("Vendor Mapping", test_vendor_mapping()))
    results.append(("Direct Call", test_direct_yfinance()))
    results.append(("Config Check", test_config()))
    
    # Summary
    print("\n" + "=" * 80)
    print("📊 TEST SUMMARY")
    print("=" * 80)
    
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name:20s}: {status}")
    
    all_passed = all(passed for _, passed in results)
    print("\n" + "=" * 80)
    if all_passed:
        print("🎉 ALL TESTS PASSED - Fix is working!")
        print("=" * 80)
        print("\n✅ The 404 error should now be RESOLVED:")
        print("   - yfinance now has get_fundamentals implementation")
        print("   - Interface correctly maps yfinance to get_fundamentals")
        print("   - Config uses yfinance as primary vendor")
        print("   - No more fallback to openai (which caused 404)")
    else:
        print("❌ SOME TESTS FAILED - Fix needs attention")
        print("=" * 80)
    
    return all_passed

if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)
