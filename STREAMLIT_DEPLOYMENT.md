# Streamlit Cloud Setup Instructions

## Step 1: Deploy to Streamlit Cloud

1. Go to: https://share.streamlit.io
2. Sign in with GitHub
3. Click "New app"
4. Select repository: `jimmy00415/TradingAgents`
5. Branch: `main`
6. Main file: `streamlit_app.py`

## Step 2: Add Azure OpenAI Secret

Before clicking "Deploy", configure the secret:

1. Click "Advanced settings"
2. Go to "Secrets" tab
3. Paste this content:

```toml
AZURE_OPENAI_API_KEY = "YOUR_AZURE_KEY_HERE"
```

4. **Replace `YOUR_AZURE_KEY_HERE`** with your actual Azure OpenAI KEY 1 from Azure Portal
5. Click "Save"
6. Click "Deploy"

## Step 3: Wait for Deployment

- Deployment takes 2-3 minutes
- You'll get a URL like: `https://jimmy00415-tradingagents.streamlit.app`

## Your Azure OpenAI Details

- **Endpoint**: https://jimmy00415.openai.azure.com/
- **Location**: eastus
- **API Version**: 2024-05-01-preview
- **KEY 1**: Copy from Azure Portal > Keys and Endpoint page

## Local Development

For local testing, the app will read from `.env` file (already configured).

Run locally:
```bash
streamlit run streamlit_app.py
```

## Troubleshooting

If you see "AZURE_OPENAI_API_KEY not found":
1. Check Streamlit Cloud > App > Settings > Secrets
2. Ensure the key is pasted correctly (no extra spaces)
3. Reboot the app after adding secrets
