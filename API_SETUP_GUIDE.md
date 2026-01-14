# 🔑 TradingAgents API Keys Setup Guide

## 📋 Current API Keys Summary

### **Primary LLM Provider (HKBU GenAI/Azure OpenAI)**
```
OPENAI_API_KEY=bb806427-7dd1-4f92-86a2-aa8748197cca
AZURE_OPENAI_API_KEY=bb806427-7dd1-4f92-86a2-aa8748197cca
AZURE_OPENAI_ENDPOINT=https://genai.hkbu.edu.hk/api/v0/rest
AZURE_API_VERSION=2024-12-01-preview
```

### **Data Providers**
```
ALPHA_VANTAGE_API_KEY=5GK3NBVL9YVJI3QV
FINNHUB_API_KEY=d227u3pr01qt86776u90d227u3pr01qt86776u9g
```

### **Social Media (Reddit)**
```
REDDIT_CLIENT_ID=iFpgQbdAlpGiKCEFHufQxw
REDDIT_CLIENT_SECRET=KP6W-3Op9G_kNCAHQUuVYq-OBNz_NA
REDDIT_USER_AGENT=TradingAgents:v1.0:by/u/Old-Reflection1388
```

---

## 🚀 Quick Setup Instructions (For Team Members)

### **Step 1: Clone the Repository**
```bash
git clone https://github.com/jimmy00415/TradingAgents.git
cd TradingAgents
```

### **Step 2: Create Python Virtual Environment**

**Using conda (Recommended):**
```bash
conda create -n tradingagents python=3.13
conda activate tradingagents
```

**Or using venv:**
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/Mac
python -m venv .venv
source .venv/bin/activate
```

### **Step 3: Install Dependencies**
```bash
pip install -r requirements.txt
```

### **Step 4: Configure API Keys**

**Option A: Quick Setup (Use Shared Keys)**

Create a `.env` file in the project root directory and copy these keys:

```bash
# Windows Command Prompt
copy NUL .env
notepad .env

# Windows PowerShell
New-Item -Path .env -ItemType File
notepad .env

# Linux/Mac
touch .env
nano .env
```

Then paste the following into the `.env` file:

```dotenv
# =============================================================================
# TRADINGAGENTS ENVIRONMENT CONFIGURATION
# =============================================================================

# -----------------------------------------------------------------------------
# LLM Provider API Keys (REQUIRED)
# -----------------------------------------------------------------------------

# HKBU GenAI Platform (Azure OpenAI Compatible)
OPENAI_API_KEY=bb806427-7dd1-4f92-86a2-aa8748197cca
AZURE_OPENAI_API_KEY=bb806427-7dd1-4f92-86a2-aa8748197cca
AZURE_OPENAI_ENDPOINT=https://genai.hkbu.edu.hk/api/v0/rest
AZURE_API_VERSION=2024-12-01-preview

# -----------------------------------------------------------------------------
# Data Provider API Keys (REQUIRED)
# -----------------------------------------------------------------------------

# Alpha Vantage API Key
ALPHA_VANTAGE_API_KEY=5GK3NBVL9YVJI3QV

# Finnhub API Key (Optional but recommended)
FINNHUB_API_KEY=d227u3pr01qt86776u90d227u3pr01qt86776u9g

# -----------------------------------------------------------------------------
# Social Media API (Optional)
# -----------------------------------------------------------------------------

# Reddit API Credentials
REDDIT_CLIENT_ID=iFpgQbdAlpGiKCEFHufQxw
REDDIT_CLIENT_SECRET=KP6W-3Op9G_kNCAHQUuVYq-OBNz_NA
REDDIT_USER_AGENT=TradingAgents:v1.0:by/u/Old-Reflection1388

# -----------------------------------------------------------------------------
# TradingAgents Configuration
# -----------------------------------------------------------------------------

TRADINGAGENTS_RESULTS_DIR=./results
```

**Option B: Use Your Own API Keys**

If you prefer to use your own API keys, follow the detailed instructions in the [Getting Your Own API Keys](#-getting-your-own-api-keys) section below.

### **Step 5: Verify Setup**

Test that everything is working:

```bash
# Test the CLI
python -m cli.main

# Or run a quick analysis
python main.py
```

---

## 🔐 Getting Your Own API Keys

If you want to use your own API keys instead of shared ones:

### **1. HKBU GenAI / Azure OpenAI (Required)**

**For HKBU Students:**
- Contact your IT department or instructor
- Access: https://genai.hkbu.edu.hk
- Copy your API key from the dashboard

**For Azure OpenAI Users:**
1. Create an Azure account: https://azure.microsoft.com
2. Create an Azure OpenAI resource
3. Get your API key and endpoint from Azure Portal
4. Update in `.env`:
   ```
   AZURE_OPENAI_API_KEY=your_key_here
   AZURE_OPENAI_ENDPOINT=your_endpoint_here
   ```

**For Standard OpenAI Users:**
1. Go to: https://platform.openai.com/api-keys
2. Create an API key
3. Update `tradingagents/default_config.py`:
   - Change `"llm_provider": "azure"` to `"llm_provider": "openai"`
4. Add to `.env`:
   ```
   OPENAI_API_KEY=your_openai_key_here
   ```

### **2. Alpha Vantage API (Required)**

Alpha Vantage provides free financial data:

1. Visit: https://www.alphavantage.co/support/#api-key
2. Enter your email and get instant free API key
3. TradingAgents users get **increased rate limits** (60 requests/min, no daily limits)
4. Add to `.env`:
   ```
   ALPHA_VANTAGE_API_KEY=your_key_here
   ```

### **3. Finnhub API (Optional but Recommended)**

Provides enhanced insider trading data:

1. Visit: https://finnhub.io/register
2. Sign up for free account
3. Copy API key from dashboard
4. Add to `.env`:
   ```
   FINNHUB_API_KEY=your_key_here
   ```

### **4. Reddit API (Optional)**

For social media sentiment analysis:

1. Create a Reddit account if you don't have one
2. Go to: https://www.reddit.com/prefs/apps
3. Click "Create App" or "Create Another App"
4. Fill in:
   - **Name**: TradingAgents
   - **App type**: Script
   - **Description**: Trading analysis bot
   - **About URL**: (leave empty)
   - **Redirect URI**: http://localhost:8080
5. Click "Create app"
6. Copy your credentials:
   - **Client ID**: (under app name)
   - **Client Secret**: (in the app details)
7. Add to `.env`:
   ```
   REDDIT_CLIENT_ID=your_client_id
   REDDIT_CLIENT_SECRET=your_client_secret
   REDDIT_USER_AGENT=TradingAgents:v1.0:by/u/your_reddit_username
   ```

---

## ✅ Verification Steps

After setting up your API keys:

1. **Check if .env file exists:**
   ```bash
   # Windows PowerShell
   Test-Path .env
   
   # Linux/Mac
   ls -la .env
   ```

2. **Verify keys are loaded:**
   ```bash
   python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('OpenAI Key:', os.getenv('OPENAI_API_KEY')[:20] + '...' if os.getenv('OPENAI_API_KEY') else 'NOT SET')"
   ```

3. **Run a test:**
   ```bash
   python -m cli.main
   ```

---

## 🔧 Troubleshooting

### **Error: "AuthenticationError: Invalid API key"**

**Solution:**
1. Open `.env` file
2. Verify the API key is correct (no extra spaces)
3. Ensure no quotes around the key value
4. Restart the application

```bash
# Check your current key
Get-Content .env | Select-String "AZURE_OPENAI_API_KEY"

# Update if needed
notepad .env
```

### **Error: ".env file not found"**

**Solution:**
1. Make sure you're in the project root directory
2. Create the .env file:
   ```bash
   # Windows
   New-Item -Path .env -ItemType File
   
   # Linux/Mac
   touch .env
   ```
3. Copy the API keys from [Step 4](#step-4-configure-api-keys)

### **Error: "Rate limit exceeded" (Alpha Vantage)**

**Solution:**
- The shared key has high limits, but you can get your own free key
- Visit: https://www.alphavantage.co/support/#api-key
- Mention you're using TradingAgents for increased limits

### **Python Environment Issues**

**Solution:**
```bash
# Verify Python version (need 3.10+)
python --version

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# If using conda
conda env remove -n tradingagents
conda create -n tradingagents python=3.13
conda activate tradingagents
pip install -r requirements.txt
```

---

## 📁 File Structure

After setup, your directory should look like:

```
TradingAgents/
├── .env                          # ✅ Your API keys (NEVER COMMIT THIS)
├── .env.example                  # Template file
├── .gitignore                    # Protects .env from being committed
├── API_SETUP_GUIDE.md           # This file
├── requirements.txt              # Python dependencies
├── main.py                       # Main script
├── cli/                          # CLI application
├── tradingagents/               # Core package
│   ├── default_config.py        # Configuration settings
│   └── dataflows/               # Data providers
└── results/                      # Analysis results (auto-created)
```

---

## ⚠️ Important Security Notes

1. **NEVER commit `.env` to GitHub** - It's already in `.gitignore`
2. **Don't share API keys publicly** - Keep them secure
3. **Use your own keys for production** - Shared keys are for team testing only
4. **Rotate keys periodically** - For security best practices
5. **Monitor API usage** - Check your quota consumption

---

## 🆘 Getting Help

If you encounter issues:

1. Check the [TROUBLESHOOTING.md](TROUBLESHOOTING.md) file
2. Verify all API keys are correctly formatted
3. Ensure `.env` file is in the project root
4. Check that your virtual environment is activated
5. Contact the project maintainer with error messages

---

## 📚 Additional Resources

- **Project README**: [README.md](README.md)
- **Setup Guide**: [SETUP_GUIDE.md](SETUP_GUIDE.md)
- **Alpha Vantage Docs**: https://www.alphavantage.co/documentation/
- **Azure OpenAI Docs**: https://learn.microsoft.com/en-us/azure/ai-services/openai/
- **Finnhub API Docs**: https://finnhub.io/docs/api

---

**✨ Happy Trading! 📈**
