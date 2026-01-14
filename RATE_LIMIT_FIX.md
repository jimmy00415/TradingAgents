# Rate Limit Error Fix Guide

## Error Encountered

```
openai.RateLimitError: Error code: 429
{'statusCode': 429, 'message': 'Monthly token limit exceeded'}
```

**Date**: January 14, 2026  
**Cause**: HKBU GenAI platform Azure OpenAI API key hit monthly token quota

---

## Solutions Implemented

### Option 1: Switch to Standard OpenAI (RECOMMENDED)

**Cost**: ~$0.50-$2.00 per analysis (gpt-4o pricing)

#### Steps:

1. **Get OpenAI API Key**
   - Visit: https://platform.openai.com/api-keys
   - Create account and add payment method
   - Generate new API key (starts with `sk-`)

2. **Update `streamlit_app.py`**
   ```python
   # Line 18-19
   USE_AZURE = False  # Changed from True
   os.environ['OPENAI_API_KEY'] = 'sk-YOUR_REAL_KEY_HERE'  # Line 32
   ```

3. **Redeploy on Streamlit Cloud**
   - Go to: https://share.streamlit.io
   - Click your app → Settings → Reboot
   - Or push to GitHub (auto-deploys)

#### Cost Breakdown (GPT-4o):
- Input: $2.50 per 1M tokens
- Output: $10.00 per 1M tokens
- Typical analysis: ~50K input + ~10K output = **$0.23 per run**
- With 5 AI agents: ~**$1.15 per analysis**

---

### Option 2: Wait for HKBU Quota Reset

**When**: Likely February 1, 2026 (monthly reset)

1. Change `USE_AZURE = True` in streamlit_app.py
2. Wait for quota reset
3. Redeploy

**Downside**: Team can't use app for 2+ weeks

---

### Option 3: Get New HKBU API Key

1. Contact HKBU GenAI platform support
2. Request:
   - Quota increase
   - Additional API key
   - Upgrade to higher tier

---

## Current Configuration

### Azure OpenAI (HKBU) - ❌ Rate Limited
```python
USE_AZURE = False  # Currently disabled
AZURE_OPENAI_API_KEY = 'bb806427-7dd1-4f92-86a2-aa8748197cca'
AZURE_OPENAI_ENDPOINT = 'https://genai.hkbu.edu.hk/api/v0/rest'
```

### Standard OpenAI - ✅ Active
```python
USE_AZURE = False
OPENAI_API_KEY = 'sk-YOUR_KEY_HERE'  # MUST REPLACE
```

---

## Quick Fix Checklist

- [ ] Get OpenAI API key from https://platform.openai.com/api-keys
- [ ] Edit `streamlit_app.py` line 32: Replace `sk-YOUR_OPENAI_API_KEY_HERE` with real key
- [ ] Verify `USE_AZURE = False` on line 19
- [ ] Test locally: `streamlit run streamlit_app.py`
- [ ] Push to GitHub: `git add streamlit_app.py` → `git commit` → `git push`
- [ ] Wait 2 minutes for Streamlit Cloud auto-deployment
- [ ] Test deployed app with sample ticker (e.g., AAPL)

---

## Testing

After making changes, test with:

```bash
# Local test
streamlit run streamlit_app.py

# Then in browser:
# Ticker: AAPL
# Date: 2026-01-13
# Model: gpt-4o
# Click "Run Analysis"
```

Expected result: Analysis completes in 2-5 minutes with no rate limit errors.

---

## Notes

- **Security**: With standard OpenAI, consider using Streamlit Secrets instead of hardcoding key
- **Cost control**: OpenAI allows setting monthly spending limits in dashboard
- **Fallback**: If OpenAI is down, can temporarily switch back to Azure by changing `USE_AZURE = True`
- **Team use**: With paid OpenAI key, no monthly limits (only per-minute rate limits which are generous)

---

## Contact

If you need help:
1. Check OpenAI status: https://status.openai.com/
2. Check HKBU GenAI platform status
3. Review API_SETUP_GUIDE.md for detailed configuration
