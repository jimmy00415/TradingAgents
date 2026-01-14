"""
TradingAgents Streamlit Web Interface
A web-based UI for running trading analysis through browser
"""

import streamlit as st
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import json

# Load environment variables
load_dotenv()

# Standard OpenAI Configuration (works from Streamlit Cloud)
# Get your API key from: https://platform.openai.com/api-keys
os.environ['OPENAI_API_KEY'] = 'sk-proj-YOUR_OPENAI_KEY_HERE'  # ⚠️ REPLACE WITH YOUR KEY

# Data source API keys (keep these)
os.environ['ALPHA_VANTAGE_API_KEY'] = '5GK3NBVL9YVJI3QV'
os.environ['FINNHUB_API_KEY'] = 'd227u3pr01qt86776u90d227u3pr01qt86776u9g'
os.environ['REDDIT_CLIENT_ID'] = 'iFpgQbdAlpGiKCEFHufQxw'
os.environ['REDDIT_CLIENT_SECRET'] = 'KP6W-3Op9G_kNCAHQUuVYq-OBNz_NA'
os.environ['REDDIT_USER_AGENT'] = 'TradingAgents:v1.0:by/u/Old-Reflection1388'

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
st.markdown("---")

# Sidebar Configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
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
    llm_model = st.selectbox(
        "LLM Model",
        options=["gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "gpt-3.5-turbo"],
        index=0,
        help="Select the OpenAI model for analysis"
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
                
                # Configure with explicit Azure OpenAI settings
                config = DEFAULT_CONFIG.copy()
                config["deep_think_llm"] = llm_model
                config["quick_think_llm"] = llm_model
                config["max_debate_rounds"] = debate_rounds
                config["max_risk_discuss_rounds"] = risk_rounds
                
                # Use standard OpenAI (not Azure)
                config["llm_provider"] = "openai"
                
                status_text.text("🤖 Initializing TradingAgents...")
                progress_bar.progress(20)
                
                # Run analysis
                ta = TradingAgentsGraph(debug=False, config=config)
                
                status_text.text("📊 Gathering market data...")
                progress_bar.progress(40)
                
                status_text.text("🧠 AI agents analyzing...")
                progress_bar.progress(60)
                
                _, decision = ta.propagate(ticker_upper, date_str)
                
                status_text.text("✅ Analysis complete!")
                progress_bar.progress(100)
                
                st.success("✅ Analysis Complete!")
                
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
                st.subheader("📄 Generated Reports")
                
                report_path = f"./results/{ticker_upper}/{date_str}/reports"
                if os.path.exists(report_path):
                    report_files = [f for f in os.listdir(report_path) if f.endswith('.md')]
                    
                    if report_files:
                        tabs = st.tabs([f"📝 {file.replace('.md', '').replace('_', ' ').title()}" for file in report_files])
                        
                        for i, file in enumerate(report_files):
                            with tabs[i]:
                                with open(os.path.join(report_path, file), 'r', encoding='utf-8') as f:
                                    content = f.read()
                                    st.markdown(content)
                    else:
                        st.info("No markdown reports generated yet.")
                else:
                    st.info("No reports directory found yet.")
                
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
