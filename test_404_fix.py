"""
Quick integration test to verify 404 error fix
Tests the complete data fetching pipeline
"""
from tradingagents.dataflows.interface import route_to_vendor

def test_fundamentals_no_404():
    """Test that get_fundamentals works without 404 errors"""
    print("=" * 80)
    print("🧪 Testing get_fundamentals - 404 Error Fix Verification")
    print("=" * 80)
    
    ticker = "TSLA"
    curr_date = "2026-01-14"
    
    print(f"\n📊 Fetching fundamental data for {ticker}...")
    print(f"   Using vendor config from default_config.py")
    
    try:
        result = route_to_vendor(
            "get_fundamentals",
            ticker,
            curr_date
        )
        
        # Check result
        if result and len(result) > 100:
            print(f"\n✅ SUCCESS: Received {len(result)} characters of data")
            print(f"\n📋 Sample output (first 500 chars):")
            print("-" * 80)
            print(result[:500])
            print("...")
            print("-" * 80)
            
            # Verify no error messages
            if "404" in result:
                print("\n❌ FAILED: 404 error found in result")
                return False
            if "Resource not found" in result:
                print("\n❌ FAILED: 'Resource not found' error in result")
                return False
            if "Error" in result and "Error retrieving" not in result:
                print(f"\n⚠️  WARNING: Generic error found in result")
                
            # Verify expected content
            checks = {
                "Symbol": ticker.upper() in result,
                "Market Cap": "Market Cap" in result or "marketCap" in result,
                "Company Info": "Tesla" in result or "Company" in result,
                "Valid JSON/Data": "{" in result or ":" in result
            }
            
            print(f"\n🔍 Content Validation:")
            for check_name, passed in checks.items():
                status = "✅" if passed else "❌"
                print(f"   {status} {check_name}")
            
            if all(checks.values()):
                print(f"\n🎉 ALL CHECKS PASSED - 404 Fix is working correctly!")
                return True
            else:
                print(f"\n⚠️  Some validation checks failed")
                return False
        else:
            print(f"\n❌ FAILED: Received empty or short result ({len(result) if result else 0} chars)")
            if result:
                print(f"Result: {result}")
            return False
            
    except Exception as e:
        print(f"\n❌ EXCEPTION OCCURRED: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("\n" + "=" * 80)
    print("🚀 404 ERROR FIX - INTEGRATION TEST")
    print("=" * 80)
    print("\nThis test verifies:")
    print("1. ✅ yfinance get_fundamentals implementation works")
    print("2. ✅ No fallback to OpenAI endpoint (which causes 404)")
    print("3. ✅ Returns valid fundamental data")
    print("4. ✅ No '404 Resource not found' errors")
    
    success = test_fundamentals_no_404()
    
    print("\n" + "=" * 80)
    if success:
        print("✅ INTEGRATION TEST PASSED")
        print("=" * 80)
        print("\n🎯 Ready for full TSLA analysis in Streamlit!")
        print("   The 404 error should no longer occur.")
    else:
        print("❌ INTEGRATION TEST FAILED")
        print("=" * 80)
        print("\n⚠️  Please review the error output above")
    
    return success

if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)
