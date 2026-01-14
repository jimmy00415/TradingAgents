"""
List all model deployments in Azure OpenAI resource
"""

from dotenv import load_dotenv
import os
import requests

load_dotenv()

print("=" * 60)
print("Azure OpenAI Deployment Lister")
print("=" * 60)

api_key = os.getenv('AZURE_OPENAI_API_KEY')
endpoint = os.getenv('AZURE_OPENAI_ENDPOINT', 'https://jimmy00415.openai.azure.com/')
api_version = os.getenv('AZURE_API_VERSION', '2025-06-01')

# Remove trailing slash if present
endpoint = endpoint.rstrip('/')

print(f"\nConfiguration:")
print(f"  Endpoint: {endpoint}")
print(f"  API Version: {api_version}")
print(f"  API Key: {'***' + api_key[-4:] if api_key else 'Not set'}")

if not api_key or not endpoint:
    print("\n✗ Azure OpenAI credentials not configured")
    exit(1)

# Try multiple endpoint formats
endpoints_to_try = [
    f"{endpoint}/openai/deployments?api-version={api_version}",
    f"{endpoint}/deployments?api-version={api_version}",
    f"{endpoint}/openai/models?api-version={api_version}",
]

print(f"\nTrying different API endpoints...")
print("-" * 60)

success = False
for list_url in endpoints_to_try:
    try:
        print(f"\nTrying: {list_url}")
        headers = {"api-key": api_key}
        
        response = requests.get(list_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            print(f"✓ Success!")
            data = response.json()
            print(f"Response keys: {list(data.keys())}")
            
            # Handle different response formats
            deployments = data.get('data', data.get('deployments', data.get('value', [])))
            
            if deployments and len(deployments) > 0:
                success = True
                print(f"\n✓ Found {len(deployments)} deployment(s):\n")
                print("=" * 60)
                
                for i, dep in enumerate(deployments, 1):
                    # Handle different response formats
                    dep_name = dep.get('id', dep.get('name', dep.get('deploymentId', 'Unknown')))
                    model = dep.get('model', dep.get('modelName', 'Unknown'))
                    status = dep.get('status', dep.get('provisioningState', 'Unknown'))
                    
                    print(f"\n{i}. Deployment Name: {dep_name}")
                    print(f"   Model: {model}")
                    print(f"   Status: {status}")
                
                print("\n" + "=" * 60)
                print("Configuration Instructions:")
                print("=" * 60)
                
                recommended_dep = deployments[0].get('id', deployments[0].get('name', deployments[0].get('deploymentId', 'Unknown')))
                
                print(f"\nUse this deployment name in your config:")
                print(f'\n1. Update test_integration.py:')
                print(f'   config["deep_think_llm"] = "{recommended_dep}"')
                print(f'   config["quick_think_llm"] = "{recommended_dep}"')
                
                print(f'\n2. Update tradingagents/default_config.py:')
                print(f'   "deep_think_llm": "{recommended_dep}",')
                print(f'   "quick_think_llm": "{recommended_dep}",')
                
                break
            else:
                print("Response has no deployments")
        else:
            print(f"  Status: {response.status_code}")
            if response.status_code == 404:
                print(f"  Not found at this endpoint")
    except Exception as e:
        print(f"  Error: {str(e)[:100]}")
        continue

if not success:
    print("\n" + "=" * 60)
    print("⚠ No Deployments Found")
    print("=" * 60)
    print("\nYour Azure OpenAI resource exists but has no model deployments.")
    print("\nTo create a deployment:")
    print("  1. Go to https://portal.azure.com")
    print("  2. Search for 'Azure OpenAI'")
    print("  3. Select your resource (Jimmy00415)")
    print("  4. Click 'Model deployments' in the left menu")
    print("  5. Click 'Create new deployment'")
    print("  6. Select a model (recommended: gpt-4o or gpt-35-turbo)")
    print("  7. Give it a deployment name (e.g., 'gpt-4o-deployment')")
    print("  8. Click 'Create'")
    print("\nOnce deployed, run this script again to get the deployment name.")

print("\n" + "=" * 60)
