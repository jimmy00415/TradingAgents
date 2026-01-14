"""
Test to verify redundant vendors are removed and DISABLE_LOCAL_SOURCES is auto-enabled
"""
print("\n" + "="*70)
print("VENDOR CLEANUP VERIFICATION TEST")
print("="*70)

# Import interface module (should auto-enable DISABLE_LOCAL_SOURCES)
import os
print(f"\nBefore import: DISABLE_LOCAL_SOURCES = {os.getenv('DISABLE_LOCAL_SOURCES')}")

from tradingagents.dataflows.interface import VENDOR_METHODS

print(f"After import:  DISABLE_LOCAL_SOURCES = {os.getenv('DISABLE_LOCAL_SOURCES')}")

# Check which methods still have 'local' vendor
print("\n" + "="*70)
print("METHODS WITH 'local' VENDOR (should be minimal)")
print("="*70)

methods_with_local = {}
for method, vendors in VENDOR_METHODS.items():
    if 'local' in vendors:
        methods_with_local[method] = vendors['local']
        
if methods_with_local:
    for method, impl in methods_with_local.items():
        impl_name = impl.__name__ if callable(impl) else [f.__name__ for f in impl]
        print(f"✓ {method}: {impl_name}")
    print(f"\nTotal: {len(methods_with_local)} methods have 'local' vendor")
else:
    print("✓ No methods have 'local' vendor!")

# Check that problematic ones were removed
print("\n" + "="*70)
print("VERIFICATION: Redundant vendors REMOVED")
print("="*70)

tests = [
    ("get_indicators", "Should NOT have 'local' (was redundant yfinance call)"),
    ("get_insider_sentiment", "Should NOT have 'local' (was redundant finnhub call)"),
    ("get_insider_transactions", "Should NOT have 'local' (was redundant finnhub call)"),
]

all_passed = True
for method, reason in tests:
    if method in VENDOR_METHODS:
        has_local = 'local' in VENDOR_METHODS[method]
        status = "❌ FAIL" if has_local else "✅ PASS"
        print(f"{status} - {method}")
        print(f"         {reason}")
        print(f"         Vendors: {list(VENDOR_METHODS[method].keys())}")
        if has_local:
            all_passed = False
    else:
        print(f"⚠️ SKIP - {method} (not found)")

# Test environment variable auto-enable
print("\n" + "="*70)
print("VERIFICATION: Auto-enable DISABLE_LOCAL_SOURCES")
print("="*70)

if os.getenv("DISABLE_LOCAL_SOURCES") == "true":
    print("✅ PASS - DISABLE_LOCAL_SOURCES is 'true'")
    print("         Auto-enabled at module import")
else:
    print(f"❌ FAIL - DISABLE_LOCAL_SOURCES is '{os.getenv('DISABLE_LOCAL_SOURCES')}'")
    print("         Should be auto-enabled to 'true'")
    all_passed = False

# Summary
print("\n" + "="*70)
if all_passed:
    print("✅ ALL TESTS PASSED - Vendor cleanup successful!")
else:
    print("❌ SOME TESTS FAILED - Review output above")
print("="*70)

print("\n💡 Expected behavior:")
print("  - DISABLE_LOCAL_SOURCES should be 'true' automatically")
print("  - get_indicators should only have: yfinance, alpha_vantage")
print("  - get_insider_* should only have: finnhub, alpha_vantage, yfinance")
print("  - 'local' vendor only for: stock_data (CSV), financial statements (SimFin), news (Reddit - filtered)")
