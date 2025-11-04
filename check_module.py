import cli.main
import os

print("Module file:", cli.main.__file__)
print("File size:", os.path.getsize(cli.main.__file__), "bytes")

with open(cli.main.__file__, 'r', encoding='utf-8') as f:
    lines = f.readlines()
    print("Total lines:", len(lines))
    
    # Check line 814
    if len(lines) > 814:
        print(f"\nLine 814: {lines[813]}")
    
    # Check line 900 (should have Unicode handling)
    if len(lines) > 900:
        print(f"\nLine 900: {lines[899]}")
        
    # Check for Unicode replacements
    content = ''.join(lines)
    if 'replace(\\u2022' in repr(content) or "'\\u2022'" in content:
        print("\n✓ Unicode bullet replacement found in code")
    else:
        print("\n✗ Unicode bullet replacement NOT found")
