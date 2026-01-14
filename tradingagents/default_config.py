import os

# Deploy gpt-4o-mini if economy mode enabled and model not deployed yet
_ECONOMY_MODE = os.getenv("ECONOMY_MODE", "true").lower() == "true"
if _ECONOMY_MODE:
    print("[INFO] Economy Mode ENABLED - using gpt-4o-mini for cost optimization")
else:
    print("[INFO] Economy Mode DISABLED - using gpt-4o for all operations")

DEFAULT_CONFIG = {
    "project_dir": os.path.abspath(os.path.join(os.path.dirname(__file__), ".")),
    "results_dir": os.getenv("TRADINGAGENTS_RESULTS_DIR", "./results"),
    "data_dir": os.getenv("TRADINGAGENTS_DATA_DIR", "./data"),
    "data_cache_dir": os.path.join(
        os.path.abspath(os.path.join(os.path.dirname(__file__), ".")),
        "dataflows/data_cache",
    ),
    # LLM settings
    "llm_provider": "azure",
    "deep_think_llm": "gpt-4o",  # Standard OpenAI model name (Foundry access)
    "quick_think_llm": "gpt-4o",  # Standard OpenAI model name (Foundry access)
    "backend_url": os.getenv("AZURE_OPENAI_ENDPOINT", "https://jimmy00415.openai.azure.com/"),
    "azure_api_version": os.getenv("AZURE_API_VERSION", "2024-10-21"),
    "azure_openai_api_key": os.getenv("AZURE_OPENAI_API_KEY"),
    # Economy Mode - for low-tier Azure deployments (S0, 10K tokens/min)
    "economy_mode": os.getenv("ECONOMY_MODE", "true").lower() == "true",  # Default ON for cost savings
    "economy_config": {
        "researcher_model": "gpt-4o-mini",  # 70% cheaper, fast data gathering
        "analyst_model": "gpt-4o-mini",     # Good enough for analysis
        "decision_model": "gpt-4o",         # Keep quality for final decision
        "data_lookback_days": 30,           # Reduce from default 180 days
        "max_news_articles": 15,            # Limit news to reduce prompt size
        "skip_extended_reflection": True,   # Disable extra LLM reflection calls
    },
    # Debate and discussion settings
    "max_debate_rounds": 1,
    "max_risk_discuss_rounds": 1,
    "max_recur_limit": 100,
    # Data vendor configuration
    # Category-level configuration (default for all tools in category)
    "data_vendors": {
        "core_stock_apis": "yfinance",       # Options: yfinance, alpha_vantage, local
        "technical_indicators": "yfinance",  # Options: yfinance, alpha_vantage, local
        "fundamental_data": "yfinance",      # Changed from alpha_vantage - yfinance works better, no rate limits
        "news_data": "alpha_vantage,google", # Multi-source: primary=alpha_vantage, fallback=google
    },
    # Tool-level configuration (takes precedence over category-level)
    "tool_vendors": {
        "get_insider_sentiment": "finnhub",        # Finnhub has superior insider data
        "get_insider_transactions": "finnhub",     # Finnhub provides detailed transaction info
        "get_global_news": "google",               # Google News is fast and reliable (no Reddit dependency)
        "get_company_news": "alpha_vantage,google", # Multi-source with fallback
        # Example: "get_stock_data": "alpha_vantage",  # Override category default
        # Example: "get_news": "openai",               # Override category default
    },
}
