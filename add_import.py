#!/usr/bin/env python3
"""Add missing import re to cli/main.py"""

# Read the file
with open('cli/main.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find where to insert import re (after import datetime)
new_lines = []
re_added = False

for line in lines:
    new_lines.append(line)
    if not re_added and line.strip() == 'import datetime':
        new_lines.append('import re\n')
        re_added = True

# Write back
with open('cli/main.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("✅ Added 'import re' to cli/main.py")
