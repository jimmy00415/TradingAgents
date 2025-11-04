#!/usr/bin/env python3
"""Fix the llm_provider assignment in cli/main.py"""

import re

# Read the file
with open('cli/main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find and replace the problematic section
# Pattern 1: Replace the return dict line
content = content.replace(
    '"llm_provider": selected_llm_provider.lower(),',
    '"llm_provider": internal_provider,\n        "llm_provider_internal": internal_provider,\n        "llm_provider_display": display_provider,'
)

# Pattern 2: Add normalization logic before "# Step 6"
normalization_code = '''
    def normalize_provider(name: str) -> str:
        if not name:
            return ""
        return re.sub(r"[^a-z0-9]+", "", name.lower())

    normalized_provider = normalize_provider(selected_llm_provider)

    # Map provider name to internal format (normalized to avoid spacing/punctuation issues)
    provider_map = {
        normalize_provider("HKBU GenAI (School Platform)"): "azure",  # HKBU uses Azure OpenAI format
        normalize_provider("HKBU GenAI (Azure Compatible)"): "azure",
        normalize_provider("Azure (HKBU GenAI)"): "azure",
        normalize_provider("HKBU GenAI"): "azure",
        normalize_provider("OpenAI"): "openai",
        normalize_provider("Anthropic"): "anthropic",
        normalize_provider("Google"): "google",
        normalize_provider("OpenRouter"): "openrouter",
        normalize_provider("Ollama"): "ollama",
    }

    internal_provider = provider_map.get(normalized_provider)

    if internal_provider is None:
        if backend_url and "genai.hkbu.edu.hk" in backend_url.lower():
            internal_provider = "azure"
        elif "hkbu" in normalized_provider:
            internal_provider = "azure"
        else:
            internal_provider = selected_llm_provider.strip().lower()

    display_provider = selected_llm_provider.strip()

    # Debug output for provider mapping
    console.print(f"\\n[cyan]Provider Mapping Debug:[/cyan]")
    console.print(f"  Selected: '{display_provider}'")
    console.print(f"  Normalized: '{normalized_provider}'")
    console.print(f"  Mapped to: '{internal_provider}'")

'''

# Insert normalization code before "# Step 6"
if 'def normalize_provider' not in content:
    content = content.replace(
        '    # Step 6: Thinking agents',
        normalization_code + '    # Step 6: Thinking agents'
    )

# Pattern 3: Update select_thinking_agent calls to use internal_provider
content = content.replace(
    'selected_shallow_thinker = select_shallow_thinking_agent(selected_llm_provider)',
    'selected_shallow_thinker = select_shallow_thinking_agent(internal_provider)'
)
content = content.replace(
    'selected_deep_thinker = select_deep_thinking_agent(selected_llm_provider)',
    'selected_deep_thinker = select_deep_thinking_agent(internal_provider)'
)

# Write back
with open('cli/main.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Fixed cli/main.py")
print("   - Added provider normalization logic")
print("   - Updated return dictionary to use internal_provider")
print("   - Updated thinking agent calls")
