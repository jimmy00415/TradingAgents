# Streamlit Cloud Deployment Guide

## ✅ Local Testing Complete

The Streamlit app is running locally at: **http://localhost:8502**

Test it locally first before deploying to the cloud!

---

## 📦 Deploy to Streamlit Cloud

### Step 1: Prepare Repository

1. **Commit and push all changes to GitHub:**
   ```bash
   git add .
   git commit -m "Configure Streamlit app for deployment"
   git push origin main
   ```

2. **Verify these files are in your repository:**
   - ✅ `streamlit_app.py` (updated with correct API version)
   - ✅ `requirements.txt` (all dependencies)
   - ✅ `tradingagents/` (source code)
   - ✅ `.env.example` (template for reference)

---

### Step 2: Deploy to Streamlit Cloud

1. **Go to:** https://share.streamlit.io

2. **Sign in** with your GitHub account

3. **Click "New app"**

4. **Configure app:**
   - Repository: `TauricResearch/TradingAgents`
   - Branch: `main`
   - Main file: `streamlit_app.py`

5. **Before deploying, click "Advanced settings"**

---

### Step 3: Configure Secrets

Click on "Advanced settings" → "Secrets" tab and paste:

```toml
# Azure OpenAI API Key (REQUIRED)
AZURE_OPENAI_API_KEY = "your_azure_openai_key_here"

# Alpha Vantage API Key (REQUIRED for fundamental data)
ALPHA_VANTAGE_API_KEY = "your_alpha_vantage_key_here"

# Finnhub API Key (OPTIONAL for enhanced data)
FINNHUB_API_KEY = "your_finnhub_key_here"
```

**Important:** Replace with your actual API keys! Get them from:
- Azure OpenAI: Azure Portal → Your OpenAI Resource → Keys and Endpoint
- Alpha Vantage: https://www.alphavantage.co/support/#api-key
- Finnhub: https://finnhub.io/register

---

### Step 4: Deploy

1. Click **"Save"** in the secrets section
2. Click **"Deploy"**
3. Wait 2-3 minutes for deployment

You'll get a URL like: `https://tradingagents.streamlit.app`

---

## 🔧 Configuration Details

### Azure OpenAI Settings (Configured in App)
- **Endpoint:** https://jimmy00415.openai.azure.com/
- **API Version:** 2024-10-21 ✅ (Tested and working)
- **Deployment:** gpt-4o
- **Model Version:** 2024-11-20

### Rate Limits
- **Token limit:** 1000 tokens/minute (S0 tier)
- **Request limit:** 1 request per 10 seconds

💡 **Tip:** For production use, consider upgrading your Azure OpenAI deployment tier to avoid rate limits.

---

## 🧪 Testing the Deployed App

Once deployed, test with:
1. Select a ticker (e.g., AAPL)
2. Choose a date
3. Configure LLM settings (keep default gpt-4o)
4. Click "Run Analysis"

**Note:** First analysis may take 2-3 minutes due to:
- Data fetching
- Multiple agent processing
- LLM API calls

---

## 🐛 Troubleshooting

### Error: "AZURE_OPENAI_API_KEY not found"
- Go to: App Settings → Secrets
- Verify the key is correctly pasted
- Reboot the app after adding secrets

### Error: "Rate Limit Reached"
- This is normal for S0 tier
- Wait 60 seconds between analyses
- Or upgrade your Azure deployment

### Error: "404 Resource not found"
- Check Azure OpenAI deployment exists
- Run: `az cognitiveservices account deployment show --name Jimmy00415 --resource-group TradingAgent --deployment-name gpt-4o`

### App is slow or timing out
- Rate limits are in effect
- Consider using gpt-35-turbo (faster, cheaper)
- Reduce `max_debate_rounds` in advanced settings

---

## 🔄 Updating the Deployed App

After making changes:
```bash
git add .
git commit -m "Your update message"
git push origin main
```

Streamlit Cloud will automatically redeploy!

---

## 💰 Cost Considerations

### Azure OpenAI (Current Setup)
- **Model:** gpt-4o
- **Deployment:** Standard (S0 tier)
- **Limits:** 1000 tokens/min
- **Cost:** Pay-per-token

### Recommendations:
1. **For testing:** Keep current setup (works fine with rate limits)
2. **For production:** Upgrade to higher tier or PTU (Provisioned Throughput Units)
3. **To reduce costs:** Use gpt-35-turbo for quick analysis

---

## 📝 Local Development

To run locally:
```bash
# Activate virtual environment
.venv\Scripts\activate

# Run Streamlit
streamlit run streamlit_app.py
```

The app will automatically use your `.env` file for credentials.

---

## ✅ Deployment Checklist

- [ ] All changes committed and pushed to GitHub
- [ ] `requirements.txt` is up to date
- [ ] Azure OpenAI deployment is active
- [ ] API keys are ready
- [ ] Streamlit Cloud account connected to GitHub
- [ ] Secrets configured in Streamlit Cloud
- [ ] App deployed successfully
- [ ] Test analysis runs without errors

---

## 🎉 You're Ready!

Your TradingAgents app is now ready for deployment to Streamlit Cloud!

**Next steps:**
1. Test locally at http://localhost:8502
2. Commit & push to GitHub
3. Deploy to Streamlit Cloud
4. Share your app URL!
