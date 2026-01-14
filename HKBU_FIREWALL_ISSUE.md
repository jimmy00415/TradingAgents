# HKBU GenAI Firewall Issue - Resolution

## Problem

HKBU GenAI platform (`https://genai.hkbu.edu.hk/api/v0/rest`) is **blocked by firewall** when accessed from Streamlit Cloud:

```
openai.PermissionDeniedError: Access Denied
Denied Reason: WP (Web Protection)
IP Address: 35.197.92.111 (Streamlit Cloud/Google Cloud)
Reference Code: 0.b221d517.1768363278.2cbc59d0
```

### Root Cause

HKBU GenAI platform has **IP whitelist restrictions**:
- ✅ **Allowed**: HKBU campus network IPs
- ❌ **Blocked**: External cloud IPs (Streamlit Cloud, AWS, Azure, etc.)

The API key `4821b42b-7279-4a5a-a715-35e48c4426fa` works on campus but is blocked from cloud deployments.

---

## Solution: Use Standard OpenAI API

### 1. Get OpenAI API Key

Visit: https://platform.openai.com/api-keys

1. Create account (if needed)
2. Add payment method
3. Generate new API key (starts with `sk-proj-...`)
4. Copy the key (shown only once!)

### 2. Update `streamlit_app.py`

Replace HKBU configuration:

```python
# Line 17-19
os.environ['OPENAI_API_KEY'] = 'sk-proj-YOUR_REAL_KEY_HERE'  # Replace with your key
```

### 3. Redeploy

```bash
git add streamlit_app.py
git commit -m "Switch from HKBU Azure to standard OpenAI"
git push origin main
```

Wait 2 minutes for Streamlit Cloud auto-deployment.

---

## Cost Comparison

### HKBU GenAI (Azure)
- ✅ **Free** (but campus-only)
- ❌ **Blocked** from cloud deployments
- ❌ Monthly token limits

### Standard OpenAI
- ✅ **Works** from anywhere (cloud, local, mobile)
- ✅ **No IP restrictions**
- ✅ **No monthly limits** (pay-as-you-go)
- 💰 **Cost**: ~$0.50-$2.00 per analysis

### GPT-4o Pricing (Recommended Model)
- **Input**: $2.50 per 1M tokens
- **Output**: $10.00 per 1M tokens
- **Typical analysis**: 50K input + 10K output = **~$0.23**
- **With 5 AI agents**: ~**$1.15 per complete analysis**

### Cost Control
- Set spending limits: https://platform.openai.com/settings/organization/billing/limits
- Track usage: https://platform.openai.com/usage
- Example budget: $50/month = ~40 analyses

---

## Alternative: Local Development with HKBU

If you want to use HKBU API for free:

### Option 1: Run Locally on Campus
```bash
# On HKBU campus network
streamlit run streamlit_app.py
```

### Option 2: VPN to HKBU Network
1. Connect to HKBU VPN
2. Run locally: `streamlit run streamlit_app.py`
3. Share via `ngrok` or similar tunneling service

### Option 3: Contact HKBU IT
Ask to whitelist Streamlit Cloud IP range:
- Email: hotline@hkbu.edu.hk
- Request: Whitelist `35.197.0.0/16` for GenAI API access
- ⚠️ Unlikely to be approved for external services

---

## Testing After Fix

1. Get OpenAI API key
2. Update line 19 in `streamlit_app.py`
3. Test locally first:
   ```bash
   streamlit run streamlit_app.py
   # Try ticker: AAPL, Date: 2026-01-13, Model: gpt-4o
   ```
4. If local test works, push to GitHub
5. Wait 2 mins for Streamlit Cloud deployment
6. Test deployed app

---

## Models Available

### Standard OpenAI Models (Recommended)
- **gpt-4o** - Best performance, $0.23 per analysis
- **gpt-4o-mini** - Faster, cheaper ($0.05 per analysis)
- **gpt-4-turbo** - Balanced performance
- **gpt-3.5-turbo** - Cheapest ($0.01 per analysis, lower quality)

### HKBU Models (Campus Only)
- ~~deepseek-r1~~ - Blocked from cloud
- ~~deepseek-v3~~ - Blocked from cloud
- ~~gpt-5~~ - Not available on standard OpenAI

---

## Summary

**Problem**: HKBU GenAI blocked by campus firewall  
**Solution**: Switch to standard OpenAI API  
**Cost**: ~$1-2 per analysis (vs HKBU free but restricted)  
**Benefit**: Works from anywhere, no IP restrictions  

For team deployment, standard OpenAI is the only viable option.
