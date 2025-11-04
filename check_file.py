with open('cli/main.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    
print(f"Total lines: {len(lines)}")
print(f"\nLine 814: {lines[813]}")
print(f"Line 815: {lines[814]}")
print(f"\nLine 900 (should have chr(0x2022)): {lines[899] if len(lines) > 899 else 'N/A'}")
print(f"\nSearching for 'chr(0x2022)' in file...")
content = ''.join(lines)
if 'chr(0x2022)' in content:
    print("✓ Found chr(0x2022) - Unicode handling present")
else:
    print("✗ NOT found - Unicode handling missing")
