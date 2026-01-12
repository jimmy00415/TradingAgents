# TradingAgents Setup Guide

This guide will help you set up TradingAgents correctly, especially after cloning from GitHub.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [API Configuration](#api-configuration)
4. [Verification](#verification)
5. [Troubleshooting](#troubleshooting)

## Prerequisites

- Python 3.10 or higher (Python 3.13 recommended)
- Git
- pip (Python package manager)
- conda (optional, but recommended for environment management)

## Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/TauricResearch/TradingAgents.git
cd TradingAgents
```

### Step 2: Create Virtual Environment

Using conda (recommended):
```bash
conda create -n tradingagents python=3.13
conda activate tradingagents
```

Or using venv:
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

## API Configuration

TradingAgents requires API keys for data sources and LLM services. **You must configure these before running the system.**

### Required API Keys

1. **ALPHA_VANTAGE_API_KEY** - For fundamental and news data
2. **AZURE_OPENAI_API_KEY** - For LLM agents (HKBU GenAI or Azure OpenAI)

### Optional API Keys

3. **FINNHUB_API_KEY** - For enhanced insider sentiment and transaction data

### Setup Method 1: Using .env File (Recommended)

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` with your favorite text editor and replace the placeholders:
   ```bash
   # Open with notepad on Windows
   notepad .env
   
   # Or use VS Code
   code .env
   ```

3. Your `.env` file should look like this:
   ```bash
   # Required APIs
   ALPHA_VANTAGE_API_KEY=your_actual_alpha_vantage_key_here
   AZURE_OPENAI_API_KEY=your_actual_azure_openai_key_here
   
   # Optional APIs
   # FINNHUB_API_KEY=your_actual_finnhub_key_here
   ```

### Setup Method 2: Using Environment Variables

Set environment variables in your shell:

**Windows PowerShell:**
```powershell
$env:ALPHA_VANTAGE_API_KEY="your_actual_alpha_vantage_key_here"
$env:AZURE_OPENAI_API_KEY="your_actual_azure_openai_key_here"
```

**Windows Command Prompt:**
```cmd
set ALPHA_VANTAGE_API_KEY=your_actual_alpha_vantage_key_here
set AZURE_OPENAI_API_KEY=your_actual_azure_openai_key_here
```

**Linux/Mac:**
```bash
export ALPHA_VANTAGE_API_KEY="your_actual_alpha_vantage_key_here"
export AZURE_OPENAI_API_KEY="your_actual_azure_openai_key_here"
```

## Getting Your API Keys

### 1. Alpha Vantage API Key (Required)

1. Go to [https://www.alphavantage.co/support/#api-key](https://www.alphavantage.co/support/#api-key)
2. Fill out the form and submit
3. You'll receive your free API key immediately
4. **Note**: TradingAgents users get increased rate limits (60 requests/min, no daily limits) thanks to Alpha Vantage's open-source support program

### 2. Azure OpenAI / HKBU GenAI API Key (Required)

**If you have HKBU GenAI access:**
- Contact your institution administrator for your API key
- The default endpoint `https://genai.hkbu.edu.hk/api/v0/rest` is already configured

**If you want to use standard OpenAI:**
1. Go to [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Sign up or log in
3. Create a new API key
4. Modify `llm_provider` in `tradingagents/default_config.py`:
   ```python
   "llm_provider": "openai",  # Change from "azure" to "openai"
   ```
5. Set your OpenAI key as `AZURE_OPENAI_API_KEY` (the code will handle it correctly)

**If you want to use Azure OpenAI Service:**
1. Go to [https://azure.microsoft.com/en-us/products/ai-services/openai-service](https://azure.microsoft.com/en-us/products/ai-services/openai-service)
2. Set up your Azure OpenAI resource
3. Get your API key and endpoint
4. Update your `.env` file:
   ```bash
   AZURE_OPENAI_API_KEY=your_azure_key
   AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com
   ```

### 3. Finnhub API Key (Optional)

1. Go to [https://finnhub.io/register](https://finnhub.io/register)
2. Sign up for a free account
3. Get your API key from the dashboard
4. Add to `.env` file:
   ```bash
   FINNHUB_API_KEY=your_finnhub_key_here
   ```

**Note**: Finnhub is optional. If not configured, the system will use yfinance for insider data instead.

## Verification

### Test Your Setup

1. **Test API Keys:**
   ```bash
   python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('Alpha Vantage:', 'OK' if os.getenv('ALPHA_VANTAGE_API_KEY') else 'MISSING'); print('Azure OpenAI:', 'OK' if os.getenv('AZURE_OPENAI_API_KEY') else 'MISSING')"
   ```

2. **Run the CLI:**
   ```bash
   python -m cli.main
   ```
   
   You should see the TradingAgents interface without any API key errors.

3. **Run a Simple Test:**
   ```bash
   python main.py
   ```

### Expected Output

If everything is configured correctly:
- ✅ No "API key not configured" errors
- ✅ CLI interface loads successfully
- ✅ Data fetching works without authentication errors

## Troubleshooting

### Common Issues

#### Issue 1: "ALPHA_VANTAGE_API_KEY environment variable is not set"

**Solution:**
- Make sure you created the `.env` file in the project root (not in a subdirectory)
- Verify the `.env` file contains `ALPHA_VANTAGE_API_KEY=your_key` (no quotes needed)
- If using environment variables directly, make sure they're set in the same terminal session where you run the code

#### Issue 2: "Azure OpenAI configuration requires endpoint, API version, and API key"

**Solution:**
- Ensure `AZURE_OPENAI_API_KEY` is set in your `.env` file
- If using a custom Azure endpoint, also set:
  ```bash
  AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com
  AZURE_API_VERSION=2024-12-01-preview
  ```
- If using standard OpenAI, change `llm_provider` to `"openai"` in `tradingagents/default_config.py`

#### Issue 3: "Finnhub API key not configured"

**Solution:**
- This is optional. If you don't need Finnhub data, you can ignore this warning
- To resolve, get a free Finnhub API key and add it to your `.env` file
- The system will fallback to yfinance for insider data

#### Issue 4: Rate Limiting / API Quota Exceeded

**Solution:**
- Alpha Vantage free tier has rate limits (60 requests/min for TradingAgents users)
- Wait a minute and try again
- Consider reducing `max_debate_rounds` in `tradingagents/default_config.py` for testing
- Use `gpt-4.1-mini` instead of `gpt-4` to reduce API costs during development

#### Issue 5: Import Errors

**Solution:**
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt

# If using conda, ensure you're in the right environment
conda activate tradingagents
```

## Configuration Options

### Customize LLM Settings

Edit `tradingagents/default_config.py`:

```python
DEFAULT_CONFIG = {
    # LLM Provider: "azure", "openai", "ollama", or "openrouter"
    "llm_provider": "azure",
    
    # Model Selection
    "deep_think_llm": "gpt-4.1",        # For complex analysis
    "quick_think_llm": "gpt-4.1-mini",  # For fast operations
    
    # Debate Settings
    "max_debate_rounds": 1,  # Increase for deeper analysis (costs more)
    "max_risk_discuss_rounds": 1,
    
    # Backend URL (for Azure/HKBU GenAI)
    "backend_url": "https://genai.hkbu.edu.hk/api/v0/rest",
}
```

### Customize Data Vendors

You can change which APIs to use for different data types:

```python
DEFAULT_CONFIG = {
    # ...
    "data_vendors": {
        "core_stock_apis": "yfinance",       # Options: yfinance, alpha_vantage, local
        "technical_indicators": "yfinance",  # Options: yfinance, alpha_vantage, local
        "fundamental_data": "alpha_vantage", # Options: openai, alpha_vantage, local
        "news_data": "alpha_vantage,google", # Multi-source: primary,fallback
    },
    
    # Override specific tools
    "tool_vendors": {
        "get_insider_sentiment": "finnhub",        # Use Finnhub for insider data
        "get_insider_transactions": "finnhub",
    },
}
```

## Security Best Practices

1. **Never commit `.env` file to Git**
   - The `.gitignore` file already excludes `.env`
   - Double-check before pushing: `git status`

2. **Rotate API keys periodically**
   - Especially if you accidentally expose them

3. **Use different API keys for different environments**
   - Development keys for testing
   - Production keys for live trading (research purposes only)

4. **Limit API key permissions**
   - Only grant necessary permissions on your API provider dashboards

## Next Steps

Once your setup is complete:

1. **Read the main [README.md](README.md)** for usage examples
2. **Explore the CLI**: `python -m cli.main`
3. **Try the Python API**: See [README.md#python-usage](README.md#python-usage)
4. **Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)** for common issues

## Getting Help

- **Discord**: Join our community at [https://discord.com/invite/hk9PGKShPK](https://discord.com/invite/hk9PGKShPK)
- **GitHub Issues**: Report bugs at [https://github.com/TauricResearch/TradingAgents/issues](https://github.com/TauricResearch/TradingAgents/issues)
- **Documentation**: Visit [https://tauric.ai/](https://tauric.ai/)

---

**Happy Trading! 🚀📈**

*Remember: TradingAgents is for research purposes only and should not be considered financial advice.*
