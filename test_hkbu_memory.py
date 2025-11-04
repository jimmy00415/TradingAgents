"""Test HKBU memory handling - embeddings disabled for HKBU GenAI."""

def test_hkbu_memory_detection():
    """Test that HKBU backend is properly detected."""
    from tradingagents.agents.utils.memory import FinancialSituationMemory
    
    # Test HKBU detection
    hkbu_config = {'backend_url': 'https://genai.hkbu.edu.hk/api/v0/rest'}
    hkbu_memory = FinancialSituationMemory('test_hkbu', hkbu_config)
    
    assert hkbu_memory.is_hkbu == True, "Failed to detect HKBU backend"
    assert hkbu_memory.embedding is None, "Embedding should be None for HKBU"
    assert hkbu_memory.client is None, "Client should be None for HKBU"
    print("✓ HKBU backend properly detected")

def test_hkbu_memory_operations():
    """Test that memory operations safely handle HKBU."""
    from tradingagents.agents.utils.memory import FinancialSituationMemory
    
    hkbu_config = {'backend_url': 'https://genai.hkbu.edu.hk/api/v0/rest'}
    memory = FinancialSituationMemory('test_ops', hkbu_config)
    
    # These should not raise errors
    try:
        embedding = memory.get_embedding("test text")
        assert embedding is None, "get_embedding should return None for HKBU"
        print("✓ get_embedding returns None for HKBU")
        
        memory.add_situations([("situation", "advice")])
        print("✓ add_situations safely skips for HKBU")
        
        results = memory.get_memories("current situation")
        assert results == [], "get_memories should return empty list for HKBU"
        print("✓ get_memories returns empty list for HKBU")
        
    except Exception as e:
        print(f"✗ Error during HKBU memory operations: {e}")
        raise

def test_non_hkbu_memory():
    """Test that non-HKBU backends still work normally."""
    from tradingagents.agents.utils.memory import FinancialSituationMemory
    
    # Test Ollama detection
    ollama_config = {'backend_url': 'http://localhost:11434/v1'}
    ollama_memory = FinancialSituationMemory('test_ollama', ollama_config)
    
    assert ollama_memory.is_hkbu == False, "Should not detect HKBU for Ollama"
    assert ollama_memory.embedding == "nomic-embed-text", "Should use Ollama embedding"
    assert ollama_memory.client is not None, "Client should be initialized"
    print("✓ Ollama backend works normally")

if __name__ == "__main__":
    print("="*60)
    print("HKBU Memory Handling Test")
    print("="*60)
    
    test_hkbu_memory_detection()
    test_hkbu_memory_operations()
    test_non_hkbu_memory()
    
    print("\n" + "="*60)
    print("✓ All tests passed! HKBU memory handling is robust.")
    print("="*60)
    print("\n[INFO] Memory/embeddings are disabled for HKBU GenAI")
    print("[INFO] This is expected - HKBU uses /deployments/{model}/embeddings")
    print("[INFO] Core trading functionality is not affected")
