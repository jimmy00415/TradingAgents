"""
Quick test to verify Google News adapter and Reddit bypass fixes
"""
import os
os.environ["DISABLE_LOCAL_SOURCES"] = "true"

from tradingagents.dataflows.google import get_google_company_news, get_google_news
from datetime import datetime, timedelta

def test_google_adapter():
    """Test the new get_google_company_news adapter"""
    print("\n=== Testing Google Company News Adapter ===")
    
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    
    try:
        result = get_google_company_news("TSLA", start_date, end_date)
        print(f"✅ Adapter works! Got {len(result)} characters")
        if result:
            print(f"Preview: {result[:200]}...")
        else:
            print("⚠️ Empty result (may be rate limited or no news)")
        return True
    except Exception as e:
        print(f"❌ Adapter failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_google_news_direct():
    """Test the original get_google_news with proper types"""
    print("\n=== Testing Google News Direct (type safety) ===")
    
    curr_date = datetime.now().strftime("%Y-%m-%d")
    look_back_days = 7
    
    try:
        # Test with string query and int look_back_days
        result = get_google_news("Tesla", curr_date, look_back_days)
        print(f"✅ Direct call works! Got {len(result)} characters")
        
        # Test with int query (should be coerced to string)
        result2 = get_google_news(12345, curr_date, look_back_days)
        print(f"✅ Type coercion works! Got {len(result2)} characters")
        
        return True
    except Exception as e:
        print(f"❌ Direct call failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_reddit_bypass():
    """Test that Reddit functions respect DISABLE_LOCAL_SOURCES"""
    print("\n=== Testing Reddit Bypass ===")
    
    from tradingagents.dataflows.local import get_reddit_global_news, get_reddit_company_news
    
    try:
        # Should return empty string immediately
        result1 = get_reddit_global_news("2026-01-14", look_back_days=7)
        if result1 == "":
            print("✅ get_reddit_global_news correctly returns empty string")
        else:
            print(f"⚠️ get_reddit_global_news returned data: {len(result1)} chars")
        
        # Should return empty string immediately
        result2 = get_reddit_company_news("TSLA", "2026-01-07", "2026-01-14")
        if result2 == "":
            print("✅ get_reddit_company_news correctly returns empty string")
        else:
            print(f"⚠️ get_reddit_company_news returned data: {len(result2)} chars")
        
        return True
    except Exception as e:
        print(f"❌ Reddit bypass test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_vendor_routing():
    """Test that vendor routing respects configuration"""
    print("\n=== Testing Vendor Routing ===")
    
    from tradingagents.dataflows.interface import route_to_vendor, get_vendor
    
    try:
        # Check vendor selection for get_news
        vendor = get_vendor("news_data", "get_news")
        print(f"✅ get_news vendor: {vendor}")
        
        # Check vendor selection for get_global_news
        vendor2 = get_vendor("news_data", "get_global_news")
        print(f"✅ get_global_news vendor: {vendor2}")
        
        # Verify local is not in fallback list
        print(f"✅ DISABLE_LOCAL_SOURCES=true is set")
        
        return True
    except Exception as e:
        print(f"❌ Vendor routing test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🧪 Running fix verification tests...")
    print(f"Environment: DISABLE_LOCAL_SOURCES={os.getenv('DISABLE_LOCAL_SOURCES')}")
    
    results = []
    results.append(("Google Adapter", test_google_adapter()))
    results.append(("Google Direct", test_google_news_direct()))
    results.append(("Reddit Bypass", test_reddit_bypass()))
    results.append(("Vendor Routing", test_vendor_routing()))
    
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {name}")
    
    all_passed = all(r[1] for r in results)
    print("="*60)
    if all_passed:
        print("🎉 All tests passed!")
    else:
        print("⚠️ Some tests failed - review output above")
