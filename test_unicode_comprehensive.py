"""Comprehensive test for all Unicode character replacements."""
import tempfile
from pathlib import Path

# All problematic Unicode characters that LLMs commonly generate
UNICODE_CHARS = {
    '\u2011': '-',   # Non-breaking hyphen
    '\u2013': '-',   # En dash
    '\u2014': '-',   # Em dash
    '\u2018': "'",   # Left single quotation mark
    '\u2019': "'",   # Right single quotation mark
    '\u201c': '"',   # Left double quotation mark
    '\u201d': '"',   # Right double quotation mark
    '\u2022': '*',   # Bullet point
    '\u2026': '...'  # Horizontal ellipsis
}

def clean_unicode(text):
    """Replace problematic Unicode characters with ASCII equivalents."""
    for unicode_char, replacement in UNICODE_CHARS.items():
        text = text.replace(unicode_char, replacement)
    return text

def test_individual_characters():
    """Test each Unicode character individually."""
    print("\n=== Testing Individual Unicode Characters ===")
    for unicode_char, expected in UNICODE_CHARS.items():
        test_text = f"Test {unicode_char} character"
        cleaned = clean_unicode(test_text)
        actual = cleaned.replace("Test ", "").replace(" character", "")
        status = "✓" if actual == expected else "✗"
        print(f"{status} U+{ord(unicode_char):04X} ({unicode_char}): '{actual}' == '{expected}'")
        assert actual == expected, f"Failed for U+{ord(unicode_char):04X}"

def test_realistic_content():
    """Test realistic LLM output with multiple Unicode characters."""
    print("\n=== Testing Realistic LLM Output ===")
    
    # Simulate actual LLM analysis output
    llm_output = """
    Analysis of SPY—a comprehensive review:
    • Market trend: Bullish momentum
    • Key levels: Support at $450–$455
    • Analyst says: "We're seeing strong signals" with 95% confidence
    • Summary… the outlook remains positive
    """
    
    cleaned = clean_unicode(llm_output)
    
    # Verify replacements
    assert '\u2014' not in cleaned, "Em dash not replaced"
    assert '\u2022' not in cleaned, "Bullet not replaced"
    assert '\u2013' not in cleaned, "En dash not replaced"
    assert '\u201c' not in cleaned, "Left quote not replaced"
    assert '\u201d' not in cleaned, "Right quote not replaced"
    assert '\u2026' not in cleaned, "Ellipsis not replaced"
    
    print("✓ All Unicode characters replaced in realistic content")
    print(f"Original length: {len(llm_output)}, Cleaned length: {len(cleaned)}")

def test_file_writing():
    """Test writing cleaned content to UTF-8 file."""
    print("\n=== Testing File Writing ===")
    
    test_content = "SPY Analysis • Key points:\n• Price: $450–$455\n• Trend: \"Bullish\"\n• Outlook… positive"
    cleaned = clean_unicode(test_content)
    
    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', delete=False, suffix='.log') as f:
        temp_path = Path(f.name)
        f.write(cleaned)
    
    # Read back and verify
    read_content = temp_path.read_text(encoding='utf-8')
    assert read_content == cleaned
    
    temp_path.unlink()
    print("✓ Successfully wrote and read cleaned content to/from UTF-8 file")

def test_ascii_fallback():
    """Test that content can be safely encoded as ASCII after cleaning."""
    print("\n=== Testing ASCII Fallback ===")
    
    problematic_text = "Price: $450–$455 • Analyst: \"Strong buy\""
    cleaned = clean_unicode(problematic_text)
    
    # Should not raise exception
    try:
        ascii_bytes = cleaned.encode('ascii')
        print(f"✓ Cleaned text safely encodes to ASCII: {ascii_bytes}")
    except UnicodeEncodeError as e:
        print(f"✗ Failed to encode as ASCII: {e}")
        raise

def test_edge_cases():
    """Test edge cases like multiple consecutive Unicode chars."""
    print("\n=== Testing Edge Cases ===")
    
    # Multiple consecutive Unicode characters
    test_cases = [
        ("———", "---"),  # Three em dashes
        ("•••", "***"),  # Three bullets
        ("\"quoted\"", '"quoted"'),  # Smart quotes
        ("…………", "............"),  # Four ellipses = 12 dots
    ]
    
    for original, expected in test_cases:
        cleaned = clean_unicode(original)
        status = "✓" if cleaned == expected else "✗"
        print(f"{status} '{original}' → '{cleaned}' (expected: '{expected}')")
        assert cleaned == expected

if __name__ == "__main__":
    print("="*60)
    print("Comprehensive Unicode Character Replacement Test")
    print("="*60)
    
    test_individual_characters()
    test_realistic_content()
    test_file_writing()
    test_ascii_fallback()
    test_edge_cases()
    
    print("\n" + "="*60)
    print("✓ All tests passed! Unicode handling is robust.")
    print("="*60)
