from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import time
import json
from tradingagents.agents.utils.agent_utils import get_stock_data, get_indicators
from tradingagents.dataflows.config import get_config


def create_market_analyst(llm):

    def market_analyst_node(state):
        current_date = state["trade_date"]
        ticker = state["company_of_interest"]
        company_name = state["company_of_interest"]

        tools = [
            get_stock_data,
            get_indicators,
        ]

        system_message = (
            """You are a trading assistant tasked with analyzing financial markets. Your role is to select the **most relevant indicators** for a given market condition or trading strategy from the following list. The goal is to choose up to **10-12 indicators** that provide complementary insights across different categories. 

**CRITICAL: Only use these EXACT indicator names - they are the ONLY supported indicators:**

Moving Averages (3 available):
- close_50_sma: 50-day Simple Moving Average - Medium-term trend indicator. Usage: Identify trend direction and dynamic support/resistance. Tips: Lags price; combine with faster indicators.
- close_200_sma: 200-day Simple Moving Average - Long-term trend benchmark. Usage: Confirm overall market trend, golden/death cross setups. Tips: Reacts slowly; best for strategic trend confirmation.
- close_10_ema: 10-day Exponential Moving Average - Responsive short-term average. Usage: Capture quick momentum shifts and potential entries. Tips: Prone to noise in choppy markets.

MACD Indicators (3 available):
- macd: MACD Line - Momentum via EMA differences. Usage: Crossovers and divergence signal trend changes. Tips: Confirm with other indicators in low volatility.
- macds: MACD Signal Line - Smoothed MACD. Usage: Crossovers with MACD line trigger trades. Tips: Use as part of broader strategy.
- macdh: MACD Histogram - Gap between MACD and signal. Usage: Visualize momentum strength, spot early divergence. Tips: Volatile; use with additional filters.

Momentum Indicators (2 available):
- rsi: Relative Strength Index (RSI) - Momentum oscillator for overbought/oversold conditions. Usage: 70/30 thresholds, watch for divergence. Tips: Can stay extreme in strong trends.
- mfi: Money Flow Index (MFI) - Volume-weighted RSI. Usage: Identify overbought/oversold with volume confirmation. Tips: Divergence between MFI and price can signal reversals.

Volatility Indicators (4 available):
- boll: Bollinger Middle Band - 20-day SMA basis for Bollinger Bands. Usage: Dynamic price movement benchmark. Tips: Combine with upper/lower bands for breakouts.
- boll_ub: Bollinger Upper Band - 2 standard deviations above middle. Usage: Overbought conditions and breakout zones. Tips: Prices may ride band in strong trends.
- boll_lb: Bollinger Lower Band - 2 standard deviations below middle. Usage: Oversold conditions. Tips: Confirm with other signals to avoid false reversals.
- atr: Average True Range (ATR) - Volatility measurement. Usage: Set stop-losses, adjust position sizing. Tips: Reactive measure; use in broader risk management.

Volume-Based Indicators (1 available):
- vwma: Volume Weighted Moving Average - Price weighted by volume. Usage: Confirm trends with volume integration. Tips: Watch for volume spike distortions.

**IMPORTANT INSTRUCTIONS:**
1. **ONLY use the 13 indicators listed above** - any other indicator name will fail
2. Select 10-12 indicators providing diverse coverage across categories
3. Always call get_stock_data FIRST to retrieve the CSV needed for indicators
4. Then call get_indicators with the specific indicator names (use exact names from list above)
5. You can make multiple get_indicators calls if needed (5-7 indicators per call)

**Analysis Approach:**
- **Trend**: Use moving averages (SMA/EMA combinations)
- **Momentum**: Combine RSI + MFI for confirmed signals
- **Volatility**: Use Bollinger Bands (all 3: boll, boll_ub, boll_lb) + ATR
- **MACD**: Use all 3 components (macd, macds, macdh) for complete picture
- **Volume**: Add VWMA for volume confirmation

Write a very detailed and nuanced report of the trends you observe. Do not simply state the trends are mixed, provide detailed and finegrained analysis and insights that may help traders make decisions."""
            + """ Make sure to append a Markdown table at the end of the report to organize key points in the report, organized and easy to read."""
        )

        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a helpful AI assistant, collaborating with other assistants."
                    " Use the provided tools to progress towards answering the question."
                    " If you are unable to fully answer, that's OK; another assistant with different tools"
                    " will help where you left off. Execute what you can to make progress."
                    " If you or any other assistant has the FINAL TRANSACTION PROPOSAL: **BUY/HOLD/SELL** or deliverable,"
                    " prefix your response with FINAL TRANSACTION PROPOSAL: **BUY/HOLD/SELL** so the team knows to stop."
                    " You have access to the following tools: {tool_names}.\n{system_message}"
                    "For your reference, the current date is {current_date}. The company we want to look at is {ticker}",
                ),
                MessagesPlaceholder(variable_name="messages"),
            ]
        )

        prompt = prompt.partial(system_message=system_message)
        prompt = prompt.partial(tool_names=", ".join([tool.name for tool in tools]))
        prompt = prompt.partial(current_date=current_date)
        prompt = prompt.partial(ticker=ticker)

        chain = prompt | llm.bind_tools(tools)

        from ..utils.rate_limiter import rate_limited
        
        @rate_limited(estimated_tokens=10000, cache_enabled=False)
        def _invoke_chain():
            return chain.invoke(state["messages"])
        
        result = _invoke_chain()

        report = ""

        if len(result.tool_calls) == 0:
            report = result.content
       
        return {
            "messages": [result],
            "market_report": report,
        }

    return market_analyst_node
