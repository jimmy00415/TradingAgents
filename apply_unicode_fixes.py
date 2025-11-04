"""Apply Unicode handling fixes to cli/main.py"""
import re

# Read the current file
with open('cli/main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Pattern 1: Fix save_message_decorator - add encoding and Unicode cleaning
pattern1 = r'''(def save_message_decorator\(obj, func_name\):.*?timestamp, message_type, content = obj\.messages\[-1\].*?content = content\.replace\("\\n", " "\).*?)(\s+with open\(log_file, "a"\) as f:)'''

replacement1 = r'''\1
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
                content_safe = content.encode('ascii', 'replace').decode('ascii')\2'''

# Apply fix
content = re.sub(pattern1, replacement1, content, flags=re.DOTALL)

# Pattern 2: Fix save_tool_call_decorator
pattern2 = r'''(def save_tool_call_decorator\(obj, func_name\):.*?args_str = ", "\.join.*?)(\s+with open\(log_file, "a"\) as f:)'''

replacement2 = r'''\1
            # Clean for safe writing - replace Unicode characters
            args_str = str(args_str).replace(chr(0x2011), '-').replace(chr(0x2013), '-').replace(chr(0x2014), '-')
            args_str = args_str.replace(chr(0x2018), "'").replace(chr(0x2019), "'")
            args_str = args_str.replace(chr(0x201c), '"').replace(chr(0x201d), '"')
            args_str = args_str.replace(chr(0x2022), '*').replace(chr(0x2026), '...')
            args_str = args_str.replace(chr(0x223c), '~')
            try:
                with open(log_file, "a", encoding="utf-8") as f:
                    f.write(f"{timestamp} [Tool Call] {tool_name}({args_str})\\n")
            except UnicodeEncodeError:
                args_str_safe = args_str.encode('ascii', 'replace').decode('ascii')\2'''

content = re.sub(pattern2, replacement2, content, flags=re.DOTALL)

# Pattern 3: Fix save_report_section_decorator - just add encoding
content = re.sub(
    r'with open\(report_dir / file_name, "w"\) as f:',
    'with open(report_dir / file_name, "w", encoding="utf-8") as f:',
    content
)

# Write back
with open('cli/main.py', 'w', encoding='utf-8', newline='\n') as f:
    f.write(content)

print("✓ Applied all Unicode handling fixes")
print("✓ File saved with UTF-8 encoding")
