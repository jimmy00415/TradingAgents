import sys
sys.dont_write_bytecode = True  # Disable bytecode generation
import cli.main

with open(cli.main.__file__, 'r', encoding='utf-8') as f:
    lines = f.readlines()
    
print(f"✓ Python restarted with bytecode disabled")
print(f"✓ Loaded module from: {cli.main.__file__}")
print(f"✓ Total lines in file: {len(lines)}")

# Check line 867
if len(lines) > 866:
    print(f"Line 867: {lines[866].rstrip()}")
    if 'encoding="utf-8"' in lines[865]:
        print("✓ Line 866 has UTF-8 encoding")
    else:
        print("✗ Line 866 MISSING UTF-8 encoding")
