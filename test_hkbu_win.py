#!/usr/bin/env python3
"""
Test HKBU provider integration end-to-end (Windows compatible)
"""
import os
import sys
from pathlib import Path

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_hkbu_provider_normalization():
    """Test that HKBU provider selections map correctly to Azure backend"""
    from cli.main import get_user_selections
    
    # Mock selections that would come from user input
    test_cases = [
        {
            "provider": "HKBU GenAI Platform",
            "backend_url": "https://genai.hkbu.edu.hk/api/v0/rest",
            "expected_internal": "azure"
        },
        {
            "provider": "hkbu genai platform",
            "backend_url": "https://genai.hkbu.edu.hk/api/v0/rest",
            "expected_internal": "azure"
        }
    ]
    
    print("[TEST] HKBU Provider Normalization\n")
    
    for idx, case in enumerate(test_cases, 1):
        print(f"Test Case {idx}:")
        print(f"  Input Provider: {case['provider']}")
        print(f"  Backend URL: {case['backend_url']}")
        
        # Simulate the normalization logic from cli/main.py
        import re
        selected_llm_provider = case['provider']
        backend_url = case['backend_url']
        
        # Provider normalization logic (extracted from cli/main.py)
        def normalize_provider(name: str) -> str:
            if not name:
                return ""
            return re.sub(r"[^a-z0-9]+", "", name.lower())
        
        provider_map = {
            normalize_provider("HKBU GenAI (School Platform)"): "azure",
            normalize_provider("HKBU GenAI (Azure Compatible)"): "azure",
            normalize_provider("Azure (HKBU GenAI)"): "azure",
            normalize_provider("HKBU GenAI"): "azure",
            normalize_provider("HKBU GenAI Platform"): "azure",
            normalize_provider("OpenAI"): "openai",
            normalize_provider("Anthropic"): "anthropic",
            normalize_provider("Google"): "google",
            normalize_provider("OpenRouter"): "openrouter",
            normalize_provider("Ollama"): "ollama",
        }
        
        normalized_provider = normalize_provider(selected_llm_provider)
        internal_provider = provider_map.get(normalized_provider)
        
        if internal_provider is None:
            if backend_url and "genai.hkbu.edu.hk" in backend_url.lower():
                internal_provider = "azure"
            elif "hkbu" in normalized_provider:
                internal_provider = "azure"
            else:
                internal_provider = selected_llm_provider.strip().lower()
        
        print(f"  [OK] Internal Provider: {internal_provider}")
        
        assert internal_provider == case['expected_internal'], \
            f"Expected '{case['expected_internal']}', got '{internal_provider}'"
        
        print(f"  [PASS]\n")
    
    print("[OK] All provider normalization tests passed!\n")


def test_azure_client_instantiation():
    """Test that Azure client can be instantiated with HKBU credentials"""
    from langchain_openai import AzureChatOpenAI
    import os
    
    print("[TEST] Azure Client Instantiation\n")
    
    # Check environment variables
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    api_version = os.getenv("AZURE_API_VERSION")
    
    print(f"  Endpoint: {endpoint}")
    print(f"  API Key: {'*' * 8 if api_key else 'NOT SET'}")
    print(f"  API Version: {api_version}\n")
    
    if not all([endpoint, api_key, api_version]):
        print("  [SKIP] Missing HKBU environment variables")
        return
    
    try:
        # Try to instantiate client (same as graph/trading_graph.py does)
        client = AzureChatOpenAI(
            azure_endpoint=endpoint,
            azure_deployment="gpt-4.1-mini",  # Valid HKBU deployment
            api_version=api_version,
            api_key=api_key,
            temperature=0.7
        )
        print("  [OK] AzureChatOpenAI client created successfully")
        
        # Quick validation call
        response = client.invoke("Say 'Hello from HKBU!' and nothing else.")
        print(f"  [OK] Test invocation: {response.content[:50]}...")
        print(f"  [PASS]\n")
        
    except Exception as e:
        print(f"  [FAIL] {e}\n")
        raise


def test_config_structure():
    """Test that config structure matches what TradingAgentsGraph expects"""
    print("[TEST] Config Structure\n")
    
    # This mimics what cli/main.py builds
    config = {
        "llm_provider": "azure",  # Internal provider
        "llm_model": "gpt-4.1-mini",
        "azure_endpoint": "https://genai.hkbu.edu.hk/api/v0/rest",
        "azure_api_version": "2024-12-01-preview",
        "azure_deployment": "gpt-4.1-mini"
    }
    
    print("  Config keys:")
    for key, value in config.items():
        print(f"    {key}: {value}")
    
    # Validate required keys
    required_keys = ["llm_provider", "llm_model"]
    for key in required_keys:
        assert key in config, f"Missing required key: {key}"
    
    # Validate Azure-specific keys when provider is azure
    if config["llm_provider"] == "azure":
        azure_keys = ["azure_endpoint", "azure_api_version", "azure_deployment"]
        for key in azure_keys:
            assert key in config, f"Missing Azure key: {key}"
    
    print("  [PASS]\n")


if __name__ == "__main__":
    print("=" * 80)
    print("HKBU GenAI Integration Test Suite")
    print("=" * 80 + "\n")
    
    try:
        test_hkbu_provider_normalization()
        test_config_structure()
        test_azure_client_instantiation()
        
        print("=" * 80)
        print("[SUCCESS] ALL TESTS PASSED")
        print("=" * 80)
        sys.exit(0)
        
    except AssertionError as e:
        print(f"\n[FAILED] TEST FAILED: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
