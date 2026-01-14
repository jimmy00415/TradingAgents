# Azure OpenAI Deployment Setup Guide

## Important: Azure OpenAI Uses Deployment Names

In Azure OpenAI, you must create **deployments** for each model you want to use. The deployment name can be different from the base model name.

## Step 1: Create Deployments in Azure Portal

1. Go to Azure Portal → Your Azure OpenAI Resource
2. Navigate to **"Deployments"** section
3. Click **"Create new deployment"**
4. For each model you want to use, create a deployment:

### Recommended Deployments

| Base Model | Suggested Deployment Name | Purpose |
|------------|---------------------------|---------|
| gpt-4o | `gpt-4o` | Main analysis model (deep thinking) |
| gpt-4o-mini | `gpt-4o-mini` | Quick tasks |
| gpt-35-turbo | `gpt-35-turbo` | Fast, cost-effective |
| gpt-4 | `gpt-4` | Legacy option |

## Step 2: Verify Your Deployments

In Azure Portal → Deployments, you should see:
- ✅ Deployment name (e.g., `gpt-4o`)
- ✅ Model name (e.g., `gpt-4o 2024-08-06`)
- ✅ Status: Running

## Step 3: Update TradingAgents Configuration

### Your Current Setup
- **Endpoint**: `https://jimmy00415.openai.azure.com/`
- **API Version**: `2024-05-01-preview`
- **Location**: `eastus`

### In Streamlit App
The dropdown shows your deployment names. Select the one you created in Azure.

### In .env File
```bash
AZURE_OPENAI_API_KEY=YOUR_KEY_HERE
AZURE_OPENAI_ENDPOINT=https://jimmy00415.openai.azure.com/
AZURE_API_VERSION=2024-05-01-preview
```

## Common Issues

### Error: "DeploymentNotFound" or "The API deployment for this resource does not exist"

**Cause**: The deployment name in the code doesn't match your Azure deployment name.

**Fix**:
1. Check Azure Portal → Deployments → Copy exact deployment name
2. In Streamlit, select that exact deployment name from dropdown
3. Make sure deployment status is "Running" (not "Creating" or "Failed")

### Error: "Resource not found"

**Cause**: Endpoint URL is incorrect

**Fix**: 
1. Azure Portal → Keys and Endpoint
2. Copy the exact endpoint URL
3. Update `.env` file with correct endpoint

### Error: "Invalid API version"

**Cause**: API version not supported for your deployment

**Fix**:
1. Use `2024-05-01-preview` (stable) or `2024-08-01-preview` (latest)
2. Check Azure docs for supported versions

## Model Capabilities by Deployment

### gpt-4o (Recommended)
- **Best for**: Complex analysis, deep thinking
- **Context**: 128K tokens
- **Speed**: Fast
- **Cost**: Medium

### gpt-4o-mini
- **Best for**: Quick tasks, summaries
- **Context**: 128K tokens
- **Speed**: Very fast
- **Cost**: Low

### gpt-35-turbo
- **Best for**: Simple tasks, cost-sensitive workloads
- **Context**: 16K tokens
- **Speed**: Very fast
- **Cost**: Very low

### gpt-4
- **Best for**: Legacy support
- **Context**: 8K-32K tokens
- **Speed**: Slower
- **Cost**: High

## Testing Your Deployment

### Test with Azure CLI
```bash
curl https://jimmy00415.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2024-05-01-preview \
  -H "Content-Type: application/json" \
  -H "api-key: YOUR_KEY_HERE" \
  -d '{
    "messages": [{"role": "user", "content": "Hello"}]
  }'
```

### Test with Python
```python
from openai import AzureOpenAI

client = AzureOpenAI(
    api_key="YOUR_KEY_HERE",
    api_version="2024-05-01-preview",
    azure_endpoint="https://jimmy00415.openai.azure.com/"
)

response = client.chat.completions.create(
    model="gpt-4o",  # Your deployment name
    messages=[{"role": "user", "content": "Hello"}]
)
print(response.choices[0].message.content)
```

## Deployment Best Practices

1. **Use consistent naming**: Deployment name = Model name (e.g., `gpt-4o` deployment for `gpt-4o` model)
2. **Set capacity**: Configure TPM (tokens per minute) based on your usage
3. **Monitor usage**: Azure Portal → Metrics → Monitor token consumption
4. **Set quotas**: Prevent unexpected costs by setting spending limits

## Next Steps

1. ✅ Create at least one deployment in Azure Portal
2. ✅ Update `.env` with your API key
3. ✅ Test deployment with Streamlit app
4. ✅ If successful, create additional deployments for other models

## Support

If you encounter issues:
1. Check Azure Portal → Deployments → Deployment status
2. Verify API key is correct (regenerate if needed)
3. Confirm endpoint URL format: `https://<resource-name>.openai.azure.com/`
4. Check Azure OpenAI quotas in your subscription
