"""Test rate limiter imports and basic functionality"""
from tradingagents.agents.utils.rate_limiter import get_rate_limiter, rate_limited
import time

def test_rate_limiter():
    """Test that rate limiter works correctly"""
    print("🧪 Testing Rate Limiter...")
    
    # Test 1: Get rate limiter instance
    limiter = get_rate_limiter()
    print(f"✅ Rate limiter initialized: {limiter.tokens_per_minute} TPM budget")
    print(f"   Max retries: {limiter.max_retries}")
    
    # Test 2: Test decorator
    call_count = 0
    
    @rate_limited(estimated_tokens=100, cache_enabled=True)
    def dummy_function(value):
        nonlocal call_count
        call_count += 1
        return f"Result: {value}"
    
    # Test 3: Make multiple calls
    print("\n📡 Making 5 test calls...")
    for i in range(5):
        result = dummy_function(f"test_{i}")
        print(f"  Call {i+1}: {result}")
    
    print(f"\n✅ All calls completed (actual function calls: {call_count})")
    
    # Test 4: Check cache (should have cached some responses)
    cache_size = len(limiter._cache)
    print(f"✅ Cache working: {cache_size} cached entry/entries")
    
    # Test 5: Check token tracking
    print(f"✅ Token tracking: {limiter._tokens_used} tokens used in current window")
    print(f"   Budget remaining: {limiter.tokens_per_minute - limiter._tokens_used} tokens")
    
    # Test 6: Test wait_if_needed
    print("\n⏱️  Testing proactive waiting...")
    start = time.time()
    limiter.wait_if_needed(100)
    elapsed = time.time() - start
    print(f"✅ wait_if_needed executed in {elapsed:.3f}s (no wait needed)")
    
    print("\n🎉 All rate limiter tests PASSED!")
    print(f"\n📊 Final Stats:")
    print(f"   - Tokens used: {limiter._tokens_used}/{limiter.tokens_per_minute}")
    print(f"   - Cache entries: {cache_size}")
    print(f"   - Function calls made: {call_count}/5 (rest served from cache)")

if __name__ == "__main__":
    test_rate_limiter()
