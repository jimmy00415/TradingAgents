#!/usr/bin/env python3
"""Verify the current state of get_user_selections return statement"""
import sys
sys.path.insert(0, '.')

from cli.main import get_user_selections
import inspect

# Get source code
source = inspect.getsource(get_user_selections)
lines = source.split('\n')

# Find the return statement
in_return = False
return_lines = []

for i, line in enumerate(lines):
    if 'return {' in line:
        in_return = True
    if in_return:
        return_lines.append(line)
        if '}' in line and not line.strip().endswith(','):
            break

print("=" * 80)
print("Current get_user_selections() return statement:")
print("=" * 80)
print('\n'.join(return_lines))
print("=" * 80)

# Check what it actually returns with llm_provider key
print("\n Checking 'llm_provider' key assignments:")
for line in return_lines:
    if 'llm_provider' in line:
        print(f"  {line.strip()}")
