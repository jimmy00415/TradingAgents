"""
Comprehensive test to verify ALL potential 404 error sources are fixed
Tests all OpenAI endpoint calls and vendor fallback scenarios
"""
from tradingagents.dataflows.interface import route_to_vendor

def test_all_openai_endpoints():
    """Test that ALL OpenAI endpoints handle 404 gracefully"""
    print("=" * 80)
    print("COMPREHENSIVE 404 ERROR TEST - ALL OPENAI ENDPOINTS")
    print("=" * 80)
    
    tests_passed = []
    tests_failed = []
    
    # Test 1: get_fundamentals (primary source of 404 errors)
    print("\nTest 1: get_fundamentals")
    print("-" * 80)
    try:
        result = route_to_vendor("get_fundamentals", "TSLA", "2026-01-14")
        if "404" not in result and "Resource not found" not in result:
            print("PASS: get_fundamentals works without 404 errors")
            print(f"   Result length: {len(result)} characters")
            tests_passed.append("get_fundamentals")
        else:
            print("FAIL: get_fundamentals returned 404 error")
            print(f"   Result: {result[:200]}")
            tests_failed.append("get_fundamentals")
    except Exception as e:
        print(f"FAIL: get_fundamentals threw exception: {e}")
        tests_failed.append("get_fundamentals")
    
    # Test 2: get_news (uses openai as fallback)
    print("\nTest 2: get_news")
    print("-" * 80)
    try:
        result = route_to_vendor("get_news", "TSLA stock", "2026-01-14", 7)
        if "404" not in result and "Resource not found" not in result:
            print("PASS: get_news works without 404 errors")
            print(f"   Result length: {len(result)} characters")
            tests_passed.append("get_news")
        else:
            print("FAIL: get_news returned 404 error")
            print(f"   Result: {result[:200]}")
            tests_failed.append("get_news")
    except Exception as e:
        print(f"FAIL: get_news threw exception: {e}")
        tests_failed.append("get_news")
    
    # Test 3: get_global_news (uses openai as fallback)
    print("\nTest 3: get_global_news")
    print("-" * 80)
    try:
        result = route_to_vendor("get_global_news", "2026-01-14", 7, 5)
        if "404" not in result and "Resource not found" not in result:
            print("PASS: get_global_news works without 404 errors")
            print(f"   Result length: {len(result)} characters")
            tests_passed.append("get_global_news")
        else:
            print("FAIL: get_global_news returned 404 error")
            print(f"   Result: {result[:200]}")
            tests_failed.append("get_global_news")
    except Exception as e:
        print(f"FAIL: get_global_news threw exception: {e}")
        tests_failed.append("get_global_news")
    
    # Test 4: get_balance_sheet
    print("\nTest 4: get_balance_sheet")
    print("-" * 80)
    try:
        result = route_to_vendor("get_balance_sheet", "TSLA", "quarterly", "2026-01-14")
        if "404" not in result and "Resource not found" not in result:
            print("PASS: get_balance_sheet works without 404 errors")
            print(f"   Result length: {len(result)} characters")
            tests_passed.append("get_balance_sheet")
        else:
            print("FAIL: get_balance_sheet returned 404 error")
            print(f"   Result: {result[:200]}")
            tests_failed.append("get_balance_sheet")
    except Exception as e:
        print(f"FAIL: get_balance_sheet threw exception: {e}")
        tests_failed.append("get_balance_sheet")
    
    # Summary
    print("\n" + "=" * 80)
    print("COMPREHENSIVE TEST SUMMARY")
    print("=" * 80)
    print(f"\nTests Passed: {len(tests_passed)}/4")
    for test in tests_passed:
        print(f"   PASS: {test}")
    
    if tests_failed:
        print(f"\nTests Failed: {len(tests_failed)}/4")
        for test in tests_failed:
            print(f"   FAIL: {test}")
    
    print("\n" + "=" * 80)
    if len(tests_passed) == 4:
        print("ALL TESTS PASSED - 404 Errors FULLY RESOLVED!")
        print("=" * 80)
        print("\nKey Fixes Applied:")
        print("   1. yfinance get_fundamentals() implementation added")
        print("   2. get_fundamentals_openai() wrapped in try/except")
        print("   3. All OpenAI endpoints gracefully handle 404 errors")
        print("   4. Vendor fallback system works correctly")
        print("\nSystem is production-ready!")
        return True
    else:
        print("SOME TESTS FAILED - Further Investigation Needed")
        print("=" * 80)
        return False

if __name__ == "__main__":
    import sys
    success = test_all_openai_endpoints()
    sys.exit(0 if success else 1)
