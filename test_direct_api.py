"""
Direct test of Azure OpenAI API call
"""
from dotenv import load_dotenv
import os
from openai import AzureOpenAI

load_dotenv()

api_key = os.getenv('AZURE_OPENAI_API_KEY')
endpoint = os.getenv('AZURE_OPENAI_ENDPOINT', 'https://jimmy00415.openai.azure.com/')
api_version = os.getenv('AZURE_API_VERSION', '2025-06-01')
deployment_name = "gpt-4o"

print("=" * 60)
print("Direct Azure OpenAI API Test")
print("=" * 60)
print(f"\nEndpoint: {endpoint}")
print(f"API Version: {api_version}")
print(f"Deployment: {deployment_name}")
print(f"API Key: {'***' + api_key[-4:] if api_key else 'Not set'}")

client = AzureOpenAI(
    api_key=api_key,
    api_version=api_version,
    azure_endpoint=endpoint
)

print("\nSending test request...")
try:
    response = client.chat.completions.create(
        model=deployment_name,  # This should be the deployment name
        messages=[{"role": "user", "content": "Say 'Hello'"}],
        max_tokens=10
    )
    print("✓ SUCCESS!")
    print(f"\nResponse: {response.choices[0].message.content}")
    print(f"Model: {response.model}")
    print("\n" + "=" * 60)
    print("✓ Azure OpenAI API is working correctly!")
    print("=" * 60)
except Exception as e:
    print(f"✗ FAILED: {e}")
    print(f"\nFull error: {str(e)}")
    
    # Try different API versions
    print("\n" + "=" * 60)
    print("Trying different API versions...")
    print("=" * 60)
    
    for test_version in ["2024-10-21", "2024-08-01-preview", "2024-06-01", "2024-05-13"]:
        print(f"\nTrying API version: {test_version}")
        try:
            test_client = AzureOpenAI(
                api_key=api_key,
                api_version=test_version,
                azure_endpoint=endpoint
            )
            response = test_client.chat.completions.create(
                model=deployment_name,
                messages=[{"role": "user", "content": "test"}],
                max_tokens=5
            )
            print(f"  ✓ SUCCESS with {test_version}!")
            print(f"  Response: {response.choices[0].message.content}")
            print(f"\n" + "=" * 60)
            print(f"SOLUTION: Use API version {test_version}")
            print("=" * 60)
            print(f"\nUpdate .env and default_config.py to:")
            print(f'  AZURE_API_VERSION={test_version}')
            break
        except Exception as e2:
            error_msg = str(e2)
            if "404" in error_msg:
                print(f"  ✗ Not found")
            elif "401" in error_msg:
                print(f"  ✗ Auth error")
            else:
                print(f"  ✗ Error: {error_msg[:50]}")
