#!/usr/bin/env python3
"""Test ticker input validation"""

def test_ticker_validation():
    """Test that ticker validation rejects invalid inputs"""
    import re
    
    test_cases = [
        # (input, should_be_valid, expected_output)
        ("SPY", True, "SPY"),
        ("spy", True, "SPY"),
        ("AAPL", True, "AAPL"),
        ("BRK.B", True, "BRK.B"),
        ("BRK-B", True, "BRK-B"),
        ('"SPY"', True, "SPY"),  # Quoted should be stripped
        ("'AAPL'", True, "AAPL"),
        ("D:/Pycharm project/TradingAgents/.venv/Scripts/activate.bat", False, None),
        ("/usr/bin/python", False, None),
        ("C:\\Windows\\System32", False, None),
        ("", True, "SPY"),  # Empty defaults to SPY
        ("test.bat", False, None),
        ("script.ps1", False, None),
    ]
    
    print("=" * 80)
    print("Testing Ticker Validation Logic")
    print("=" * 80 + "\n")
    
    passed = 0
    failed = 0
    
    for input_ticker, should_pass, expected in test_cases:
        # Simulate validation logic from get_ticker()
        raw_input = input_ticker
        ticker = str(raw_input).strip()
        
        # Remove ALL types of quotes
        ticker = ticker.strip('"').strip("'").strip('"').strip('"')
        ticker = ticker.strip()
        
        # Check validation
        is_valid = True
        
        if not ticker:
            ticker = "SPY"  # Default
            is_valid = True
        else:
            # Check for file extensions
            invalid_extensions = ['.bat', '.exe', '.ps1', '.py', '.sh', '.cmd', '.com']
            if any(ext in ticker.lower() for ext in invalid_extensions):
                is_valid = False
            # Check for path separators
            elif any(c in ticker for c in ['/', '\\', ':']):
                is_valid = False
            else:
                ticker = ticker.upper()
                if not ticker.replace('.', '').replace('-', '').isalnum():
                    is_valid = False
                elif len(ticker) > 10:
                    is_valid = False
        
        # Check result
        if is_valid == should_pass:
            if should_pass and ticker == expected:
                print(f"[PASS] '{input_ticker}' -> '{ticker}'")
                passed += 1
            elif not should_pass:
                print(f"[PASS] '{input_ticker}' -> REJECTED (as expected)")
                passed += 1
            else:
                print(f"[FAIL] '{input_ticker}' -> '{ticker}' (expected '{expected}')")
                failed += 1
        else:
            print(f"[FAIL] '{input_ticker}' -> Valid={is_valid} (expected {should_pass})")
            failed += 1
    
    print("\n" + "=" * 80)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 80)
    
    return failed == 0

if __name__ == "__main__":
    import sys
    success = test_ticker_validation()
    sys.exit(0 if success else 1)
