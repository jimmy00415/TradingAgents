"""
Test Azure OpenAI deployment availability
"""

from dotenv import load_dotenv
import os
from openai import AzureOpenAI

load_dotenv()

print("=" * 60)
print("Azure OpenAI Deployment Test")
print("=" * 60)

api_key = os.getenv('AZURE_OPENAI_API_KEY')
endpoint = os.getenv('AZURE_OPENAI_ENDPOINT', 'https://genai.hkbu.edu.hk/api/v0/rest')
api_version = os.getenv('AZURE_API_VERSION', '2024-05-01-preview')

print(f"\nConfiguration:")
print(f"  Endpoint: {endpoint}")
print(f"  API Version: {api_version}")
print(f"  API Key: {'***' + api_key[-4:] if api_key else 'Not set'}")

if not api_key or not endpoint:
    print("\n✗ Azure OpenAI credentials not configured")
    exit(1)

# Common deployment names to test
deployment_names_to_test = [
    "gpt-4o",
    "gpt-4o-mini",
    "gpt-4",
    "gpt-4-turbo",
    "gpt-35-turbo",
    "gpt-4-32k",
]

print(f"\nTesting deployments...")
print("-" * 60)

client = AzureOpenAI(
    api_key=api_key,
    api_version=api_version,
    azure_endpoint=endpoint
)

working_deployments = []

for deployment in deployment_names_to_test:
    try:
        response = client.chat.completions.create(
            model=deployment,
            messages=[{"role": "user", "content": "test"}],
            max_tokens=5
        )
        print(f"✓ {deployment:20s} - Available")
        working_deployments.append(deployment)
    except Exception as e:
        error_msg = str(e)
        if "DeploymentNotFound" in error_msg:
            print(f"✗ {deployment:20s} - Not found")
        elif "401" in error_msg or "Unauthorized" in error_msg:
            print(f"⚠ {deployment:20s} - Authentication error")
        elif "rate" in error_msg.lower() or "quota" in error_msg.lower():
            print(f"⚠ {deployment:20s} - Rate limit/quota exceeded")
        elif "404" in error_msg:
            # Print full error for 404 to see what it says
            print(f"✗ {deployment:20s} - Not found (404)")
        else:
            print(f"? {deployment:20s} - Error: {error_msg[:100]}")

print("-" * 60)

if working_deployments:
    print(f"\n✓ Found {len(working_deployments)} working deployment(s):")
    for dep in working_deployments:
        print(f"  - {dep}")
    print(f"\nTo use these, update your config:")
    print(f'  config["deep_think_llm"] = "{working_deployments[0]}"')
    print(f'  config["quick_think_llm"] = "{working_deployments[0]}"')
else:
    print("\n✗ No working deployments found.")
    print("\nPlease check:")
    print("  1. Your Azure OpenAI endpoint is correct")
    print("  2. Your API key has proper permissions")
    print("  3. The deployment names in your Azure instance")
    print("\nYou can find your deployment names in the Azure Portal:")
    print("  Azure Portal → Your Azure OpenAI Resource → Model deployments")

print("=" * 60)
