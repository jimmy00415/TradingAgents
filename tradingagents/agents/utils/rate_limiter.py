"""
Intelligent Rate Limiter for Azure OpenAI API
Prevents 429 errors through token budgeting, exponential backoff, and caching
"""
import time
import hashlib
import json
from datetime import datetime, timedelta
from typing import Optional, Callable, Any
from functools import wraps
import threading

class RateLimiter:
    """
    Token-aware rate limiter with exponential backoff
    Prevents 429 errors by managing token budgets and request pacing
    """
    
    def __init__(self, tokens_per_minute: int = 500000, max_retries: int = 10):
        """
        Initialize rate limiter
        
        Args:
            tokens_per_minute: Token budget per minute (default 500K for maximum performance)
            max_retries: Maximum retry attempts for 429 errors
        """
        self.tokens_per_minute = tokens_per_minute
        self.max_retries = max_retries
        
        # Token tracking
        self._tokens_used = 0
        self._window_start = time.time()
        self._lock = threading.Lock()
        
        # Response cache (in-memory, cleared every hour)
        self._cache = {}
        self._cache_expiry = {}
        self._cache_ttl = 3600  # 1 hour
        
        print(f"[RATE_LIMITER] Initialized with {tokens_per_minute} TPM budget")
    
    def _reset_window_if_needed(self):
        """Reset token budget if 60 seconds have passed"""
        current_time = time.time()
        elapsed = current_time - self._window_start
        
        if elapsed >= 60:
            self._tokens_used = 0
            self._window_start = current_time
            print(f"[RATE_LIMITER] Token budget reset (60s window elapsed)")
    
    def _clean_cache(self):
        """Remove expired cache entries"""
        current_time = time.time()
        expired_keys = [
            key for key, expiry in self._cache_expiry.items()
            if current_time > expiry
        ]
        
        for key in expired_keys:
            del self._cache[key]
            del self._cache_expiry[key]
        
        if expired_keys:
            print(f"[RATE_LIMITER] Cleaned {len(expired_keys)} expired cache entries")
    
    def _get_cache_key(self, func_name: str, *args, **kwargs) -> str:
        """Generate cache key from function call parameters"""
        # Create deterministic hash of function name and arguments
        cache_data = {
            'func': func_name,
            'args': str(args),
            'kwargs': str(sorted(kwargs.items()))
        }
        cache_str = json.dumps(cache_data, sort_keys=True)
        return hashlib.md5(cache_str.encode()).hexdigest()
    
    def _estimate_tokens(self, text: str) -> int:
        """
        Rough token estimation (4 chars ≈ 1 token for English)
        This is conservative; actual usage may be less
        """
        return len(text) // 4 + 10  # +10 for safety margin
    
    def wait_if_needed(self, estimated_tokens: int) -> bool:
        """
        Check token budget and wait if needed
        
        Args:
            estimated_tokens: Estimated tokens for the request
            
        Returns:
            True if request can proceed, False if budget exceeded
        """
        with self._lock:
            self._reset_window_if_needed()
            
            # Check if adding this request would exceed budget
            if self._tokens_used + estimated_tokens > self.tokens_per_minute:
                wait_time = 60 - (time.time() - self._window_start)
                
                if wait_time > 0:
                    print(f"[RATE_LIMITER] Budget exceeded ({self._tokens_used}/{self.tokens_per_minute} tokens)")
                    print(f"[RATE_LIMITER] Waiting {wait_time:.1f}s for budget reset...")
                    time.sleep(wait_time + 0.5)  # +0.5s buffer
                    
                    # Reset after waiting
                    self._tokens_used = 0
                    self._window_start = time.time()
            
            # Add tokens to usage
            self._tokens_used += estimated_tokens
            return True
    
    def execute_with_backoff(
        self,
        func: Callable,
        *args,
        estimated_tokens: Optional[int] = None,
        cache_enabled: bool = True,
        **kwargs
    ) -> Any:
        """
        Execute function with exponential backoff on rate limit errors
        
        Args:
            func: Function to execute
            *args: Function arguments
            estimated_tokens: Token estimate (auto-calculated if None)
            cache_enabled: Enable response caching
            **kwargs: Function keyword arguments
            
        Returns:
            Function result
        """
        # Check cache first
        if cache_enabled:
            self._clean_cache()
            cache_key = self._get_cache_key(func.__name__, *args, **kwargs)
            
            if cache_key in self._cache:
                print(f"[RATE_LIMITER] Cache HIT for {func.__name__}")
                return self._cache[cache_key]
        
        # Auto-estimate tokens if not provided
        if estimated_tokens is None:
            # Estimate based on string arguments
            text_args = ' '.join(str(arg) for arg in args if isinstance(arg, str))
            estimated_tokens = self._estimate_tokens(text_args) if text_args else 1000
        
        # Wait if needed
        self.wait_if_needed(estimated_tokens)
        
        # Execute with exponential backoff
        for attempt in range(self.max_retries):
            try:
                result = func(*args, **kwargs)
                
                # Cache successful result
                if cache_enabled:
                    self._cache[cache_key] = result
                    self._cache_expiry[cache_key] = time.time() + self._cache_ttl
                
                return result
                
            except Exception as e:
                error_str = str(e)
                
                # Check if it's a rate limit error
                if "429" in error_str or "RateLimitError" in str(type(e).__name__):
                    # Faster exponential backoff: 0.5s base with reduced jitter
                    wait_time = (0.5 * (2 ** attempt)) + (time.time() % 0.1)  # Faster recovery
                    
                    print(f"[RATE_LIMITER] 429 Error on attempt {attempt + 1}/{self.max_retries}")
                    print(f"[RATE_LIMITER] Backing off for {wait_time:.1f}s...")
                    
                    if attempt < self.max_retries - 1:
                        time.sleep(wait_time)
                        continue
                    else:
                        print(f"[RATE_LIMITER] Max retries exceeded, raising error")
                        raise
                else:
                    # Non-rate-limit error, raise immediately
                    raise
        
        raise Exception(f"Max retries ({self.max_retries}) exceeded for {func.__name__}")


# Global rate limiter instance (shared across all calls)
_global_limiter: Optional[RateLimiter] = None

def get_rate_limiter() -> RateLimiter:
    """Get or create global rate limiter instance"""
    global _global_limiter
    
    if _global_limiter is None:
        # Get token budget from environment or use default
        import os
        tpm = int(os.getenv("AZURE_OPENAI_TPM", "500000"))  # Maximum performance mode
        _global_limiter = RateLimiter(tokens_per_minute=tpm)
    
    return _global_limiter


def rate_limited(estimated_tokens: Optional[int] = None, cache_enabled: bool = True):
    """
    Decorator to add rate limiting to any function
    
    Usage:
        @rate_limited(estimated_tokens=5000)
        def my_llm_call(prompt):
            return client.chat.completions.create(...)
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            limiter = get_rate_limiter()
            return limiter.execute_with_backoff(
                func,
                *args,
                estimated_tokens=estimated_tokens,
                cache_enabled=cache_enabled,
                **kwargs
            )
        return wrapper
    return decorator
