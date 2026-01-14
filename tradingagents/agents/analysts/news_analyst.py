from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import time
import json
from tradingagents.agents.utils.agent_utils import (
    get_news,
    get_global_news,
    get_economic_calendar,
    get_upcoming_earnings
)
from tradingagents.dataflows.config import get_config


def create_news_analyst(llm):
    def news_analyst_node(state):
        current_date = state["trade_date"]
        ticker = state["company_of_interest"]

        tools = [
            get_news,
            get_global_news,
            get_economic_calendar,
            get_upcoming_earnings,
        ]

        system_message = (
            "You are a news researcher tasked with analyzing recent news and trends over the past week, as well as upcoming market-moving events. "
            "**CRITICAL: Always call get_economic_calendar() and get_upcoming_earnings(ticker) to understand the macroeconomic and company-specific event calendar.** This context is essential for timing trades. "
            "Use get_news(query, start_date, end_date) for company-specific or targeted news searches, and get_global_news(curr_date, look_back_days, limit) for broader macroeconomic news. "
            "**Analyze upcoming events**: FOMC meetings, CPI releases, GDP reports, earnings announcements - these drive volatility and should inform trade timing. "
            "Write a comprehensive report covering:\n"
            "1. Recent company-specific news and sentiment\n"
            "2. Broader macroeconomic trends and global events\n"
            "3. **Upcoming high-impact events** (economic calendar + earnings dates)\n"
            "4. How these factors may impact the stock in the near term\n\n"
            "Do not simply state the trends are mixed, provide detailed and finegrained analysis and insights that may help traders make decisions."
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
                    "For your reference, the current date is {current_date}. We are looking at the company {ticker}",
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
            "news_report": report,
        }

    return news_analyst_node
