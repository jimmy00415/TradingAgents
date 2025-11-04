with open('cli/main.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    print(f'Total lines: {len(lines)}')
    if len(lines) > 866:
        print(f'Line 867: {lines[866].rstrip()}')
    if len(lines) > 943:
        print(f'Line 944 (should be report decorator): {lines[943].rstrip()}')
