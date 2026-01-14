"""
TradingAgents Streamlit Web Interface
A web-based UI for running trading analysis through browser
"""

import streamlit as st
import os
from datetime import datetime, timedelta
import json

# CRITICAL: Lazy imports to reduce memory footprint on Streamlit Cloud (1GB limit)
# Do NOT import heavy modules at module level - they consume RAM before app even starts

# Load environment variables (for local development)
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass  # Silently skip if .env doesn't exist (cloud deployment)

# Azure OpenAI Configuration (Personal Account)
# For local: set in .env file | For Streamlit Cloud: set in Secrets
try:
    # Try to get from Streamlit secrets first (for cloud deployment)
    AZURE_KEY = st.secrets["AZURE_OPENAI_API_KEY"]
    ALPHA_KEY = st.secrets.get("ALPHA_VANTAGE_API_KEY", "")
    FINNHUB_KEY = st.secrets.get("FINNHUB_API_KEY", "")
except (FileNotFoundError, KeyError, AttributeError):
    # Fall back to environment variables (for local development)
    AZURE_KEY = os.getenv("AZURE_OPENAI_API_KEY", "")
    ALPHA_KEY = os.getenv("ALPHA_VANTAGE_API_KEY", "")
    FINNHUB_KEY = os.getenv("FINNHUB_API_KEY", "")

os.environ['AZURE_OPENAI_API_KEY'] = AZURE_KEY
os.environ['AZURE_OPENAI_ENDPOINT'] = 'https://jimmy00415.openai.azure.com/'
os.environ['AZURE_API_VERSION'] = '2024-10-21'
os.environ['OPENAI_API_KEY'] = AZURE_KEY

# Data source API keys
os.environ['ALPHA_VANTAGE_API_KEY'] = ALPHA_KEY
os.environ['FINNHUB_API_KEY'] = FINNHUB_KEY

# Detect deployment environment and optimize configuration
IS_CLOUD = os.getenv("STREAMLIT_RUNTIME_ENV") == "cloud" or "STREAMLIT_SHARING" in os.environ

# CRITICAL: Disable local sources (Reddit) by default in ALL environments
# Local Reddit data files don't exist in most deployments and cause hangs
if os.getenv("DISABLE_LOCAL_SOURCES") is None:
    os.environ["DISABLE_LOCAL_SOURCES"] = "true"
    print("[INFO] DISABLE_LOCAL_SOURCES auto-enabled (prevents Reddit hangs)")

if IS_CLOUD:
    print("[INFO] Running in CLOUD mode - lazy loading enabled")
else:
    print("[INFO] Running in LOCAL mode")

# LAZY LOAD: Import heavy modules only when needed (after config)
@st.cache_resource(show_spinner="Loading TradingAgents framework...")
def get_default_config():
    """Lazy load default config to reduce memory footprint"""
    from tradingagents.default_config import DEFAULT_CONFIG
    
    # Cloud-optimized configuration
    if IS_CLOUD:
        DEFAULT_CONFIG["data_vendors"] = {
            "core_stock_apis": "yfinance",
            "technical_indicators": "yfinance",
            "fundamental_data": "yfinance",
            "news_data": "finnhub",
        }
    
    return DEFAULT_CONFIG

# Get config (cached, only loads once)
DEFAULT_CONFIG = get_default_config()

# Page configuration
st.set_page_config(
    page_title="TradingAgents - AI Trading Analysis",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        padding: 1rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .stButton>button {
        width: 100%;
        height: 3rem;
        font-size: 1.2rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Authentication (optional - uncomment to enable)
# def check_password():
#     """Returns `True` if the user had the correct password."""
#     def password_entered():
#         if st.session_state["password"] == "tradingagents2026":
#             st.session_state["password_correct"] = True
#             del st.session_state["password"]
#         else:
#             st.session_state["password_correct"] = False
#
#     if "password_correct" not in st.session_state:
#         st.text_input("Password", type="password", on_change=password_entered, key="password")
#         return False
#     elif not st.session_state["password_correct"]:
#         st.text_input("Password", type="password", on_change=password_entered, key="password")
#         st.error("😕 Password incorrect")
#         return False
#     else:
#         return True
#
# if not check_password():
#     st.stop()

# Header
st.markdown('<h1 class="main-header">📈 TradingAgents</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; font-size: 1.2rem;">Multi-Agent LLM Financial Trading Framework</p>', unsafe_allow_html=True)

# Add configuration status
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("API Version", os.environ.get('AZURE_API_VERSION', 'Not set'))
with col2:
    economy_mode_status = "✅ ON" if DEFAULT_CONFIG.get("economy_mode", True) else "❌ OFF"
    st.metric("Economy Mode", economy_mode_status)
with col3:
    current_model = "gpt-4o-mini/gpt-4o" if DEFAULT_CONFIG.get("economy_mode", True) else "gpt-4o"
    st.metric("Models", current_model)
with col4:
    if st.button("🔄 Clear Cache"):
        st.cache_data.clear()
        st.cache_resource.clear()
        st.success("Cache cleared!")
        st.rerun()

# Economy Mode Info
if DEFAULT_CONFIG.get("economy_mode", True):
    st.info("💡 **Economy Mode Active**: Using gpt-4o-mini for research (70% cost savings) and gpt-4o for final decisions. Perfect for low-tier Azure deployments!")

st.markdown("---")

# Sidebar Configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Economy Mode Toggle
    st.subheader("🎯 Performance Mode")
    economy_mode = st.checkbox(
        "Enable Economy Mode",
        value=DEFAULT_CONFIG.get("economy_mode", True),
        help="Use gpt-4o-mini for research/analysis (70% cheaper) and gpt-4o for final decisions. Recommended for S0 tier (10K tokens/min)."
    )
    
    if economy_mode != DEFAULT_CONFIG.get("economy_mode", True):
        DEFAULT_CONFIG["economy_mode"] = economy_mode
        os.environ["ECONOMY_MODE"] = "true" if economy_mode else "false"
        st.rerun()
    
    if economy_mode:
        st.success("✅ Cost-optimized mode active")
        st.caption("• Research: gpt-4o-mini")
        st.caption("• Analysis: gpt-4o-mini")  
        st.caption("• Decision: gpt-4o")
    else:
        st.warning("⚠️ High token usage mode")
        st.caption("• All agents: gpt-4o")
    
    st.markdown("---")
    
    # Stock Selection
    st.subheader("📊 Stock Selection")
    ticker = st.text_input("Stock Ticker", value="AAPL", help="Enter stock symbol (e.g., AAPL, TSLA, MSFT)")
    
    # Date Selection
    default_date = datetime.now() - timedelta(days=1)
    analysis_date = st.date_input(
        "Analysis Date",
        value=default_date,
        max_value=datetime.now(),
        help="Select the date for analysis"
    )
    
    st.markdown("---")
    
    # Model Settings
    st.subheader("🤖 AI Model Settings")
    
    # Azure Foundry: Direct access to OpenAI models
    llm_model = st.selectbox(
        "LLM Model",
        options=[
            "gpt-4o-mini",      # Fast & cost-effective (RECOMMENDED for rate limits)
            "gpt-4o",           # GPT-4 Optimized (10K TPM limit)
            "gpt-4-turbo",      # GPT-4 Turbo
            "gpt-4",            # GPT-4 base
            "gpt-3.5-turbo",    # Fast legacy model
            "o1-preview",       # Reasoning model
            "o1-mini",          # Compact reasoning
        ],
        index=0,
        help="gpt-4o-mini is RECOMMENDED (50K TPM) to avoid rate limits. gpt-4o has only 10K TPM."
    )
    
    debate_rounds = st.slider(
        "Debate Rounds",
        min_value=1,
        max_value=5,
        value=1,
        help="Number of debate rounds between bull/bear researchers"
    )
    
    risk_rounds = st.slider(
        "Risk Discussion Rounds",
        min_value=1,
        max_value=3,
        value=1,
        help="Number of risk management discussion rounds"
    )
    
    st.markdown("---")
    
    # Data Sources
    st.subheader("📡 Data Sources")
    st.info(f"""
    **Active Sources:**
    - Core Data: yfinance
    - Technical: yfinance
    - Fundamental: Alpha Vantage
    - News: Alpha Vantage + Google
    - Insider Data: Finnhub
    """)
    
    st.markdown("---")
    
    # About
    with st.expander("ℹ️ About TradingAgents"):
        st.markdown("""
        **TradingAgents** is a multi-agent framework that uses specialized AI agents:
        
        - **Analysts Team**: Fundamental, Sentiment, News, Technical
        - **Researchers Team**: Bull & Bear perspectives
        - **Trader**: Makes informed decisions
        - **Risk Management**: Evaluates and manages risk
        - **Portfolio Manager**: Final approval/rejection
        
        [GitHub Repository](https://github.com/TauricResearch/TradingAgents)
        """)

# Main Content
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🎯 Run Analysis")
    
    # Analysis button
    if st.button("🚀 Start Trading Analysis", type="primary"):
        ticker_upper = ticker.upper()
        date_str = analysis_date.strftime("%Y-%m-%d")
        
        # Progress tracking
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        with st.spinner("🔄 Analyzing market data... This may take 2-5 minutes..."):
            try:
                status_text.text("🔧 Configuring AI agents...")
                progress_bar.progress(10)
                
                # LAZY IMPORT: Only import TradingAgentsGraph when needed (saves memory)
                from tradingagents.graph.trading_graph import TradingAgentsGraph
                
                # Configure with explicit Azure OpenAI settings
                config = DEFAULT_CONFIG.copy()
                config["deep_think_llm"] = llm_model
                config["quick_think_llm"] = llm_model
                config["max_debate_rounds"] = debate_rounds
                config["max_risk_discuss_rounds"] = risk_rounds
                
                # Configure Azure OpenAI (Personal Account)
                config["llm_provider"] = "azure"
                config["backend_url"] = "https://jimmy00415.openai.azure.com/"
                config["azure_api_version"] = "2024-05-01-preview"
                config["azure_openai_api_key"] = AZURE_KEY
                
                status_text.text("🤖 Initializing TradingAgents...")
                progress_bar.progress(20)
                
                # Verify deployment exists with helpful error message
                try:
                    # Use st.cache_resource to cache the TradingAgentsGraph instance
                    # This reduces memory usage by not creating multiple instances
                    @st.cache_resource(show_spinner=False)
                    def create_trading_agents(config_hash):
                        return TradingAgentsGraph(debug=False, config=config)
                    
                    # Create hash of config to cache properly
                    config_hash = f"{config['llm_provider']}_{config['deep_think_llm']}_{config['max_debate_rounds']}"
                    ta = create_trading_agents(config_hash)
                except Exception as init_error:
                    if "DeploymentNotFound" in str(init_error):
                        st.error(f"❌ Azure deployment '{llm_model}' not found")
                        st.info("""
                        **To fix this issue:**
                        
                        1. Go to [Azure Portal](https://portal.azure.com)
                        2. Navigate to your Azure OpenAI resource: `jimmy00415`
                        3. Click **"Deployments"** in the left menu
                        4. Click **"Create new deployment"** or **"Deploy model"**
                        5. Create a deployment:
                           - **Deployment name**: `{model}` (must match exactly)
                           - **Model**: Select `{model}` from the list
                           - **Deployment type**: Standard
                        6. Wait for deployment to complete (~1 minute)
                        7. Return here and try again
                        
                        **Current selected model**: `{model}`
                        
                        If `{model}` is not available, create a deployment for `gpt-4o-mini` instead and select it from the dropdown.
                        """.format(model=llm_model))
                        st.stop()
                    else:
                        raise
                
                # Run analysis
                try:
                    status_text.text("📊 Gathering market data...")
                    progress_bar.progress(40)
                    
                    status_text.text("🧠 AI agents analyzing...")
                    progress_bar.progress(60)
                    
                    final_state, decision = ta.propagate(ticker_upper, date_str)
                    
                    status_text.text("✅ Analysis complete!")
                    progress_bar.progress(100)
                    
                    st.success("✅ Analysis Complete!")
                
                except Exception as e:
                    error_msg = str(e)
                    
                    # Log full error details for debugging
                    import traceback
                    print(f"\n{'='*80}")
                    print("STREAMLIT ERROR CAUGHT")
                    print(f"{'='*80}")
                    print(f"Error type: {type(e).__name__}")
                    print(f"Error message: {error_msg}")
                    print(f"\nFull traceback:")
                    print(traceback.format_exc())
                    print(f"{'='*80}\n")
                    
                    # Handle rate limit errors
                    if "429" in error_msg or "RateLimitReached" in error_msg or "RateLimitError" in str(type(e).__name__):
                        st.error("⚠️ **Rate Limit Reached**")
                        
                        # Extract which model hit the limit
                        rate_limit_model = "gpt-4o"  # Default assumption
                        if "gpt-4o-mini" in error_msg:
                            rate_limit_model = "gpt-4o-mini"
                        elif "gpt-4o" in error_msg:
                            rate_limit_model = "gpt-4o"
                        
                        st.warning(f"""
                        **Your Azure OpenAI deployment for `{rate_limit_model}` has reached its rate limit.**
                        
                        **Current capacity:**
                        - **gpt-4o**: 10,000 tokens/minute (10K TPM)
                        - **gpt-4o-mini**: 50,000 tokens/minute (50K TPM)
                        
                        **Quick fixes:**
                        1. ✅ **Switch to gpt-4o-mini** (5x higher limit) - Select in sidebar
                        2. ⏳ **Wait 60 seconds** and try again
                        3. 🔧 **Reduce complexity**: Lower debate rounds to 1
                        4. 💰 **Upgrade capacity**: [Azure Portal](https://portal.azure.com) → Jimmy00415 → Deployments → Increase TPM
                        
                        **Recommended**: Use **gpt-4o-mini** (default) to avoid this error!
                        """)
                        st.info("💡 **Tip**: gpt-4o-mini is 70% cheaper and has 5x higher rate limits, perfect for testing!")
                        st.stop()
                    else:
                        # Other errors
                        st.error(f"❌ Error during analysis: {error_msg}")
                        with st.expander("🔍 Technical Details"):
                            st.code(error_msg)
                            # Show where error occurred
                            st.markdown("**Stack Trace (last 5 lines):**")
                            tb_lines = traceback.format_exc().split('\n')
                            for line in tb_lines[-10:]:
                                if line.strip():
                                    st.code(line, language="python")
                        st.stop()
                
                # Display Trading Decision
                st.markdown("---")
                st.subheader("📋 Trading Decision")
                
                if decision and isinstance(decision, dict):
                    # Extract action
                    action = decision.get("action", "HOLD").upper()
                    
                    # Display with color
                    if "BUY" in action:
                        st.success(f"## 🟢 **BUY** {ticker_upper}")
                    elif "SELL" in action:
                        st.error(f"## 🔴 **SELL** {ticker_upper}")
                    else:
                        st.warning(f"## ⚪ **HOLD** {ticker_upper}")
                    
                    # Show key metrics
                    col_a, col_b, col_c = st.columns(3)
                    with col_a:
                        st.metric("Ticker", ticker_upper)
                    with col_b:
                        st.metric("Date", date_str)
                    with col_c:
                        st.metric("Model", llm_model)
                    
                    st.markdown("---")
                    
                    # Full decision details
                    with st.expander("📊 View Full Decision Details", expanded=True):
                        st.json(decision)
                
                # Show Generated Reports
                st.markdown("---")
                st.subheader("📄 Analysis Reports")
                
                # Display reports from final_state (in-memory, no file I/O needed)
                if final_state:
                    # Create tabs for different report types
                    report_tabs = st.tabs([
                        "📈 Market Analysis",
                        "📰 News Analysis", 
                        "📊 Fundamentals",
                        "💭 Sentiment Analysis",
                        "🤝 Investment Debate",
                        "⚠️ Risk Analysis",
                        "💼 Investment Plan",
                        "🎯 Final Decision"
                    ])
                    
                    # Market Report
                    with report_tabs[0]:
                        if final_state.get("market_report"):
                            st.markdown(final_state["market_report"])
                        else:
                            st.info("No market report available")
                    
                    # News Report
                    with report_tabs[1]:
                        if final_state.get("news_report"):
                            st.markdown(final_state["news_report"])
                        else:
                            st.info("No news report available")
                    
                    # Fundamentals Report
                    with report_tabs[2]:
                        if final_state.get("fundamentals_report"):
                            st.markdown(final_state["fundamentals_report"])
                        else:
                            st.info("No fundamentals report available")
                    
                    # Sentiment Report
                    with report_tabs[3]:
                        if final_state.get("sentiment_report"):
                            st.markdown(final_state["sentiment_report"])
                        else:
                            st.info("No sentiment report available")
                    
                    # Investment Debate
                    with report_tabs[4]:
                        if final_state.get("investment_debate_state"):
                            debate = final_state["investment_debate_state"]
                            
                            st.markdown("### 🐂 Bull Case")
                            if debate.get("bull_history"):
                                for i, msg in enumerate(debate["bull_history"], 1):
                                    with st.expander(f"Bull Argument {i}"):
                                        st.markdown(msg)
                            
                            st.markdown("### 🐻 Bear Case")
                            if debate.get("bear_history"):
                                for i, msg in enumerate(debate["bear_history"], 1):
                                    with st.expander(f"Bear Argument {i}"):
                                        st.markdown(msg)
                            
                            st.markdown("### ⚖️ Judge Decision")
                            if debate.get("judge_decision"):
                                st.success(debate["judge_decision"])
                        else:
                            st.info("No investment debate available")
                    
                    # Risk Analysis
                    with report_tabs[5]:
                        if final_state.get("risk_debate_state"):
                            risk = final_state["risk_debate_state"]
                            
                            col1, col2, col3 = st.columns(3)
                            
                            with col1:
                                st.markdown("### 🔴 Risky View")
                                if risk.get("risky_history"):
                                    for msg in risk["risky_history"]:
                                        st.info(msg)
                            
                            with col2:
                                st.markdown("### 🟢 Safe View")
                                if risk.get("safe_history"):
                                    for msg in risk["safe_history"]:
                                        st.success(msg)
                            
                            with col3:
                                st.markdown("### 🟡 Neutral View")
                                if risk.get("neutral_history"):
                                    for msg in risk["neutral_history"]:
                                        st.warning(msg)
                            
                            st.markdown("### ⚖️ Risk Manager Decision")
                            if risk.get("judge_decision"):
                                st.info(risk["judge_decision"])
                        else:
                            st.info("No risk analysis available")
                    
                    # Investment Plan
                    with report_tabs[6]:
                        if final_state.get("investment_plan"):
                            st.markdown(final_state["investment_plan"])
                        elif final_state.get("trader_investment_plan"):
                            st.markdown(final_state["trader_investment_plan"])
                        else:
                            st.info("No investment plan available")
                    
                    # Final Decision
                    with report_tabs[7]:
                        if final_state.get("final_trade_decision"):
                            st.markdown(final_state["final_trade_decision"])
                        else:
                            st.info("No final decision available")
                else:
                    st.info("No analysis state available")
                
            except Exception as e:
                st.error(f"❌ Error during analysis")
                
                # Show error details in an expander
                with st.expander("🔍 Error Details", expanded=True):
                    st.error(str(e))
                    
                    # Check for common issues
                    error_msg = str(e).lower()
                    
                    if "rate limit" in error_msg or "429" in error_msg:
                        st.warning("""
                        **⚠️ Rate Limit Issue**
                        
                        Some API providers have rate limits. The system uses fallback providers, but you may need to:
                        - Wait a few minutes and try again
                        - Use a different stock ticker
                        - Check your API key quotas
                        """)
                    
                    elif "api key" in error_msg or "401" in error_msg or "authentication" in error_msg:
                        st.warning("""
                        **⚠️ API Key Issue**
                        
                        Please check your API keys configuration:
                        - Ensure all required API keys are set
                        - Verify keys are valid and active
                        - Check API key permissions
                        """)
                    
                    elif "network" in error_msg or "connection" in error_msg:
                        st.warning("""
                        **⚠️ Network Issue**
                        
                        Unable to connect to data providers:
                        - Check your internet connection
                        - Try again in a few moments
                        - Some providers may be temporarily unavailable
                        """)
                    
                    else:
                        st.info("""
                        **💡 Troubleshooting Tips:**
                        - Try a different stock ticker (e.g., MSFT, TSLA, GOOGL)
                        - Select a recent date (last 7 days)
                        - Refresh the page and try again
                        - Check the error message above for specific details
                        """)
                    
                    # Show traceback for debugging
                    import traceback
                    with st.expander("🔧 Technical Details (for debugging)"):
                        st.code(traceback.format_exc())
                
                status_text.text("")
                progress_bar.empty()

with col2:
    st.subheader("📚 Analysis History")
    
    # Show recent analyses
    if os.path.exists("./results"):
        results = []
        
        try:
            for ticker_dir in os.listdir("./results"):
                ticker_path = os.path.join("./results", ticker_dir)
                if os.path.isdir(ticker_path):
                    for date_dir in os.listdir(ticker_path):
                        date_path = os.path.join(ticker_path, date_dir)
                        if os.path.isdir(date_path):
                            # Get modification time
                            mod_time = os.path.getmtime(date_path)
                            results.append({
                                "ticker": ticker_dir,
                                "date": date_dir,
                                "timestamp": mod_time
                            })
            
            # Sort by timestamp (most recent first)
            results.sort(key=lambda x: x["timestamp"], reverse=True)
            
            if results:
                st.markdown("**Recent Analyses:**")
                for i, result in enumerate(results[:15]):
                    with st.container():
                        if st.button(
                            f"📊 {result['ticker']} - {result['date']}",
                            key=f"history_{i}",
                            help="Click to view this analysis"
                        ):
                            st.session_state['selected_history'] = result
                            st.rerun()
            else:
                st.info("No analyses yet. Run your first analysis!")
        
        except Exception as e:
            st.warning("Unable to load history")
    else:
        st.info("No analyses yet. Run your first analysis!")
    
    st.markdown("---")
    
    # Quick Stats
    st.subheader("📊 Quick Stats")
    if os.path.exists("./results"):
        total_analyses = len(results) if 'results' in locals() else 0
        unique_tickers = len(set([r['ticker'] for r in results])) if 'results' in locals() and results else 0
        
        st.metric("Total Analyses", total_analyses)
        st.metric("Unique Tickers", unique_tickers)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p><b>TradingAgents</b> - Multi-Agent LLM Financial Trading Framework</p>
    <p>⚠️ For research and educational purposes only. Not financial advice.</p>
    <p style='font-size: 0.9rem;'>Built with Streamlit | Powered by AI</p>
</div>
""", unsafe_allow_html=True)
