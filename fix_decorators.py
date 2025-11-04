"""
Fix cli/main.py by adding Unicode character replacements to the OLD decorator at line ~807-816
"""

with open('cli/main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find and replace the OLD decorator code (without UTF-8 encoding)
old_decorator = '''    def save_message_decorator(obj, func_name):
        func = getattr(obj, func_name)
        @wraps(func)
        def wrapper(*args, **kwargs):
            func(*args, **kwargs)
            timestamp, message_type, content = obj.messages[-1]
            content = content.replace("\\n", " ")  # Replace newlines with spaces
            with open(log_file, "a") as f:
                f.write(f"{timestamp} [{message_type}] {content}\\n")
        return wrapper'''

new_decorator = '''    def save_message_decorator(obj, func_name):
        func = getattr(obj, func_name)
        @wraps(func)
        def wrapper(*args, **kwargs):
            func(*args, **kwargs)
            timestamp, message_type, content = obj.messages[-1]
            # Clean content for safe writing
            content = str(content).replace("\\n", " ")  # Replace newlines with spaces
            # Replace problematic Unicode characters with ASCII equivalents
            content = content.replace(chr(0x2011), '-')  # Non-breaking hyphen
            content = content.replace(chr(0x2013), '-')  # En dash
            content = content.replace(chr(0x2014), '-')  # Em dash
            content = content.replace(chr(0x2018), "'")  # Left single quote
            content = content.replace(chr(0x2019), "'")  # Right single quote
            content = content.replace(chr(0x201c), '"')  # Left double quote
            content = content.replace(chr(0x201d), '"')  # Right double quote
            content = content.replace(chr(0x2022), '*')  # Bullet point
            content = content.replace(chr(0x2026), '...')  # Ellipsis
            content = content.replace(chr(0x223c), '~')  # Tilde operator
            try:
                with open(log_file, "a", encoding="utf-8") as f:
                    f.write(f"{timestamp} [{message_type}] {content}\\n")
            except UnicodeEncodeError:
                # Fallback: encode with error replacement
                content_safe = content.encode('ascii', 'replace').decode('ascii')
                with open(log_file, "a", encoding="utf-8") as f:
                    f.write(f"{timestamp} [{message_type}] {content_safe}\\n")
        return wrapper'''

if old_decorator in content:
    print("✓ Found old decorator - replacing...")
    content = content.replace(old_decorator, new_decorator)
    print("✓ Replaced decorator")
else:
    print("✗ Old decorator pattern not found. Searching for variations...")
    # Try to find it with different whitespace
    if 'with open(log_file, "a") as f:' in content:
        print("  Found: with open(log_file, \"a\") without encoding")
        # We'll need to do manual fix
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if 'with open(log_file, "a") as f:' in line:
                print(f"  Line {i+1}: {line[:80]}")

# Also fix tool_call_decorator if present
old_tool_decorator = '''    def save_tool_call_decorator(obj, func_name):
        func = getattr(obj, func_name)
        @wraps(func)
        def wrapper(*args, **kwargs):
            func(*args, **kwargs)
            timestamp, tool_name, args = obj.tool_calls[-1]
            args_str = ", ".join(f"{k}={v}" for k, v in args.items())
            with open(log_file, "a") as f:
                f.write(f"{timestamp} [Tool Call] {tool_name}({args_str})\\n")
        return wrapper'''

new_tool_decorator = '''    def save_tool_call_decorator(obj, func_name):
        func = getattr(obj, func_name)
        @wraps(func)
        def wrapper(*args, **kwargs):
            func(*args, **kwargs)
            timestamp, tool_name, args = obj.tool_calls[-1]
            args_str = ", ".join(f"{k}={v}" for k, v in args.items())
            # Clean for safe writing
            args_str = str(args_str).replace(chr(0x2011), '-').replace(chr(0x2013), '-').replace(chr(0x2014), '-')
            args_str = args_str.replace(chr(0x2018), "'").replace(chr(0x2019), "'")
            args_str = args_str.replace(chr(0x201c), '"').replace(chr(0x201d), '"')
            args_str = args_str.replace(chr(0x2022), '*').replace(chr(0x2026), '...')
            args_str = args_str.replace(chr(0x223c), '~')
            try:
                with open(log_file, "a", encoding="utf-8") as f:
                    f.write(f"{timestamp} [Tool Call] {tool_name}({args_str})\\n")
            except UnicodeEncodeError:
                args_str_safe = args_str.encode('ascii', 'replace').decode('ascii')
                with open(log_file, "a", encoding="utf-8") as f:
                    f.write(f"{timestamp} [Tool Call] {tool_name}({args_str_safe})\\n")
        return wrapper'''

if old_tool_decorator in content:
    print("✓ Found old tool decorator - replacing...")
    content = content.replace(old_tool_decorator, new_tool_decorator)
    print("✓ Replaced tool decorator")

# Write back
with open('cli/main.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("\n✓ File updated and saved to disk")

# Verify
with open('cli/main.py', 'r', encoding='utf-8') as f:
    new_content = f.read()
    if 'chr(0x2022)' in new_content:
        print("✓ Verification: Unicode handling code present")
    else:
        print("✗ Verification failed: Unicode code not found")
