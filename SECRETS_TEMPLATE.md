# 🔐 Streamlit Cloud Secrets Configuration

## Copy This Template to Streamlit Cloud

Go to your deployed app → **Manage app** → **Settings** → **Secrets**

Paste this EXACT format (replace values from your .env file):

```toml
AZURE_OPENAI_API_KEY = "your_key_here"
AZURE_OPENAI_ENDPOINT = "https://jimmy00415.openai.azure.com/"
AZURE_API_VERSION = "2024-10-21"
ALPHA_VANTAGE_API_KEY = "your_key_here"
FINNHUB_API_KEY = "your_key_here"
REDDIT_CLIENT_ID = "your_id_here"
REDDIT_CLIENT_SECRET = "your_secret_here"
REDDIT_USER_AGENT = "TradingAgents-Bot"
```

## Where to Find Your Keys

### 1. Open your .env file
Location: `d:\Pycharm project\TradingAgents\.env`

### 2. Copy each value
- `AZURE_OPENAI_API_KEY` = Copy from .env line 1
- `ALPHA_VANTAGE_API_KEY` = Copy from .env line 5
- `FINNHUB_API_KEY` = Copy from .env line 6
- `REDDIT_CLIENT_ID` = Copy from .env line 8
- `REDDIT_CLIENT_SECRET` = Copy from .env line 9

### 3. Replace in template above
- Keep the **quotes** around values
- Keep the **exact spacing** (space before and after `=`)
- **NO comments** inside the TOML block

## Example (with fake keys):
```toml
AZURE_OPENAI_API_KEY = "abc123xyz456example"
AZURE_OPENAI_ENDPOINT = "https://jimmy00415.openai.azure.com/"
AZURE_API_VERSION = "2024-10-21"
ALPHA_VANTAGE_API_KEY = "ABCD1234"
FINNHUB_API_KEY = "xyz789example"
REDDIT_CLIENT_ID = "abc123example"
REDDIT_CLIENT_SECRET = "secret123example"
REDDIT_USER_AGENT = "TradingAgents-Bot"
```

## ⚠️ Common Mistakes to Avoid

❌ **WRONG**: Missing quotes
```toml
AZURE_OPENAI_API_KEY = abc123
```

❌ **WRONG**: Comments inside values
```toml
AZURE_OPENAI_API_KEY = "abc123"  # This is my key
```

❌ **WRONG**: No spaces around =
```toml
AZURE_OPENAI_API_KEY="abc123"
```

✅ **CORRECT**: Quotes, spaces, no comments
```toml
AZURE_OPENAI_API_KEY = "abc123"
```

## Quick Copy from .env

Run this command in PowerShell to see your keys:
```powershell
Get-Content .env | Select-String "AZURE_OPENAI_API_KEY|ALPHA_VANTAGE|FINNHUB|REDDIT"
```

Then manually copy each value into the Streamlit secrets template above.
