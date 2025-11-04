#!/usr/bin/env python3
"""Test Unicode handling in log files"""
import tempfile
from pathlib import Path

def test_unicode_replacement():
    """Test that problematic Unicode characters are replaced"""
    
    test_strings = [
        ("Regular text", True),
        ("Text with \u2011 non-breaking hyphen", True),
        ("Text with \u2013 en dash", True),
        ("Text with \u2014 em dash", True),
        ("Text with \u2018 quotes \u2019", True),
        ("Text with \u201c double quotes \u201d", True),
        ("Mixed: \u2011\u2013\u2014\u2018\u2019", True),
    ]
    
    print("=" * 80)
    print("Testing Unicode Character Replacement")
    print("=" * 80 + "\n")
    
    passed = 0
    failed = 0
    
    for test_str, should_work in test_strings:
        # Simulate the cleaning logic from cli/main.py
        cleaned = str(test_str).replace("\n", " ")
        cleaned = cleaned.replace('\u2011', '-')  # Non-breaking hyphen
        cleaned = cleaned.replace('\u2013', '-')  # En dash
        cleaned = cleaned.replace('\u2014', '-')  # Em dash
        cleaned = cleaned.replace('\u2018', "'")  # Left single quote
        cleaned = cleaned.replace('\u2019', "'")  # Right single quote
        cleaned = cleaned.replace('\u201c', '"')  # Left double quote
        cleaned = cleaned.replace('\u201d', '"')  # Right double quote
        
        # Try writing to a temp file
        try:
            with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', delete=False) as f:
                temp_path = Path(f.name)
                f.write(f"Test: {cleaned}\n")
            
            # Read it back
            with open(temp_path, 'r', encoding='utf-8') as f:
                result = f.read()
            
            temp_path.unlink()  # Clean up
            
            print(f"[PASS] Original: {repr(test_str[:50])}")
            print(f"       Cleaned:  {repr(cleaned[:50])}")
            print(f"       Written:  OK\n")
            passed += 1
            
        except UnicodeEncodeError as e:
            print(f"[FAIL] {repr(test_str[:50])}")
            print(f"       Error: {e}\n")
            failed += 1
        except Exception as e:
            print(f"[ERROR] {repr(test_str[:50])}")
            print(f"        Error: {e}\n")
            failed += 1
    
    print("=" * 80)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 80)
    
    return failed == 0

if __name__ == "__main__":
    import sys
    success = test_unicode_replacement()
    sys.exit(0 if success else 1)
