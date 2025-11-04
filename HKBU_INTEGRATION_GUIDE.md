# HKBU GenAI Integration - Complete Guide

## ✅ Problem Solved

**Issue**: `ValueError: Unsupported LLM provider: hkbu genai (azure compatible)`

**Root Cause**: The CLI was storing the display label ("HKBU GenAI (Azure Compatible)") in the config instead of the internal provider identifier ("azure").

**Solution**: Implemented provider normalization logic that maps HKBU selections to the Azure backend while preserving the display label for UI purposes.

---

## 🔧 Technical Changes

### Files Modified

1. **`cli/main.py`**
   - Added `normalize_provider()` function to strip special characters and normalize names
   - Created `provider_map` dictionary to map display names to internal identifiers
   - Added fallback logic to detect HKBU by URL pattern
   - Modified `get_user_selections()` to return both internal and display provider values
   - Updated `run_analysis()` to use the internal provider for config

2. **`cli/utils.py`**
   - Added "HKBU GenAI (Azure Compatible)" option to provider selection menu
   - Created HKBU-specific model menus with actual deployed models:
     - **Quick-thinking**: gpt-4.1-nano, gpt-4.1-mini, gpt-4o
     - **Deep-thinking**: gpt-5, gpt-4.1, o1, qwen3-max, deepseek-v3

3. **`tradingagents/graph/trading_graph.py`**
   - Added Azure client instantiation logic when provider is "azure"
   - Configured `AzureChatOpenAI` with HKBU endpoint, API version, and deployment names

4. **`tradingagents/default_config.py`**
   - Updated default endpoint to HKBU GenAI
   - Set default models to HKBU deployments
   - Added Azure API metadata (version, key)

### Environment Variables

Required in `.env`:
```properties
# HKBU GenAI Platform Configuration
AZURE_OPENAI_API_KEY=a294629b-f060-40d7-af4c-56232e382aee
AZURE_OPENAI_ENDPOINT=https://genai.hkbu.edu.hk/api/v0/rest
AZURE_API_VERSION=2024-12-01-preview
```

---

## 🚀 How to Use

### Method 1: Using the Batch Script (Recommended)

The `RUN_CLI.bat` script automatically clears Python cache to ensure fresh execution:

```batch
RUN_CLI.bat
```

### Method 2: PowerShell (Manual Cache Clear)

```powershell
# Clear Python cache
Get-ChildItem -Path . -Include __pycache__ -Recurse -Force | Remove-Item -Recurse -Force

# Run CLI
python -m cli.main
```

### Method 3: Standard Python

```powershell
python -m cli.main
```

**⚠️ Important**: If you see the old error after code changes, clear the Python cache first!

---

## 📋 Usage Flow

1. **Start CLI**
   ```powershell
   python -m cli.main
   ```

2. **Select Provider**
   - Choose: "HKBU GenAI (Azure Compatible)"
   - URL: `https://genai.hkbu.edu.hk/api/v0/rest`

3. **Select Models**
   
   **Quick-Thinking Engine** (for fast analysis):
   - GPT-4.1-nano (lightweight)
   - GPT-4.1-mini (balanced) ✅ **Recommended**
   - GPT-4o (standard)

   **Deep-Thinking Engine** (for reasoning):
   - GPT-5 (flagship)
   - GPT-4.1 (enterprise)
   - O1 (strategic reasoning) ✅ **Recommended**
   - Qwen3 Max (multilingual)
   - DeepSeek V3 (high-capacity)

4. **CLI will display mapping debug info:**
   ```
   Provider Mapping Debug:
     Selected: 'HKBU GenAI (Azure Compatible)'
     Normalized: 'hkbugenaiazurecompatible'
     Mapped to: 'azure'

   ═══ Configuration Debug ═══
   Provider (display): HKBU GenAI (Azure Compatible)
   Provider (internal): azure
   Backend URL: https://genai.hkbu.edu.hk/api/v0/rest
   Quick model: gpt-4.1-mini
   Deep model: o1
   ```

---

## ✅ Verification

Run the integration test suite:

```powershell
python test_hkbu_integration.py
```

Expected output:
```
================================================================================
✅ ALL TESTS PASSED
================================================================================
```

The test validates:
1. ✅ Provider normalization (display → internal)
2. ✅ Config structure (required keys present)
3. ✅ Azure client instantiation
4. ✅ Live API connection to HKBU

---

## 🐛 Troubleshooting

### Error: "ValueError: Unsupported LLM provider"

**Cause**: Python is using cached bytecode from before the fix.

**Solution**:
```powershell
# Clear all Python caches
Get-ChildItem -Path . -Include __pycache__ -Recurse -Force | Remove-Item -Recurse -Force

# Or use the batch script
.\RUN_CLI.bat
```

### Error: "Configuration for model 'xxx' is not available"

**Cause**: Using a model name that doesn't exist in HKBU's deployments.

**Solution**: Only use models from the HKBU menu in `cli/utils.py`:
- ✅ gpt-4.1-mini, gpt-4o, o1, gpt-5, deepseek-v3, qwen3-max
- ❌ gpt-4o-mini, gpt-3.5-turbo (OpenAI names, not HKBU deployments)

### Error: "401 Unauthorized" or "403 Forbidden"

**Cause**: Invalid API key or endpoint.

**Solution**: Verify `.env` contains the correct HKBU API key and endpoint.

---

## 📊 Provider Mapping Logic

```python
# Normalization removes special characters and lowercases
"HKBU GenAI (Azure Compatible)" → "hkbugenaiazurecompatible"

# Map to internal identifier
provider_map = {
    "hkbugenaiazurecompatible": "azure",
    "hkbugenai": "azure",
    "openai": "openai",
    "anthropic": "anthropic",
    ...
}

# Fallback detection
if "genai.hkbu.edu.hk" in backend_url:
    internal_provider = "azure"
```

---

## 🎯 Key Design Decisions

1. **Display vs. Internal Provider**
   - Display label shown to user: "HKBU GenAI (Azure Compatible)"
   - Internal identifier used in code: "azure"
   - Allows friendly UI while maintaining compatibility

2. **Normalization Function**
   - Strips all non-alphanumeric characters
   - Handles variations: "HKBU GenAI", "HKBU (Azure)", etc.
   - Case-insensitive matching

3. **Fallback URL Detection**
   - If normalization fails, checks backend URL
   - Any URL containing "genai.hkbu.edu.hk" → "azure"
   - Ensures robustness

4. **Azure Deployment Format**
   - HKBU uses Azure OpenAI API format
   - Endpoint: `/openai/deployments/{model}/chat/completions`
   - Requires: deployment name, API version, key

---

## 📝 Testing Checklist

- [x] Provider normalization works for all HKBU name variants
- [x] Internal provider correctly set to "azure"
- [x] Display label preserved for UI
- [x] Azure client instantiates with HKBU credentials
- [x] Live API call succeeds
- [x] Config structure matches TradingAgentsGraph expectations
- [x] Environment variables loaded correctly
- [x] Cache clearing mechanism works

---

## 🔄 Update History

**2025-10-14**
- Initial HKBU integration
- Provider normalization logic implemented
- Azure client wiring added
- Integration test suite created
- Cache clearing scripts added

---

## 📚 References

- **HKBU GenAI Endpoint**: `https://genai.hkbu.edu.hk/api/v0/rest`
- **API Format**: Azure OpenAI Compatible
- **Available Models**: See `cli/utils.py` for full list
- **Test Suite**: `test_hkbu_integration.py`
- **Runner Script**: `RUN_CLI.bat`

---

## 💡 Tips

1. **Always clear cache** after updating code
2. **Use the batch script** for guaranteed fresh runs
3. **Check debug output** to verify provider mapping
4. **Run integration tests** before making changes
5. **Use recommended models** (gpt-4.1-mini + o1) for best balance

---

**Status**: ✅ **RESOLVED** - HKBU integration fully functional
