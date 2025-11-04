from langchain_core.tools import tool
from typing import Annotated
from tradingagents.dataflows.interface import route_to_vendor

@tool
def get_news(
    ticker: Annotated[str, "Ticker symbol"],
    start_date: Annotated[str, "Start date in yyyy-mm-dd format"],
    end_date: Annotated[str, "End date in yyyy-mm-dd format"],
) -> str:
    """
    Retrieve news data for a given ticker symbol.
    Uses the configured news_data vendor.
    Args:
        ticker (str): Ticker symbol
        start_date (str): Start date in yyyy-mm-dd format
        end_date (str): End date in yyyy-mm-dd format
    Returns:
        str: A formatted string containing news data
    """
    return route_to_vendor("get_news", ticker, start_date, end_date)

@tool
def get_global_news(
    curr_date: Annotated[str, "Current date in yyyy-mm-dd format"],
    look_back_days: Annotated[int, "Number of days to look back"] = 7,
    limit: Annotated[int, "Maximum number of articles to return"] = 5,
) -> str:
    """
    Retrieve global news data.
    Uses the configured news_data vendor.
    Args:
        curr_date (str): Current date in yyyy-mm-dd format
        look_back_days (int): Number of days to look back (default 7)
        limit (int): Maximum number of articles to return (default 5)
    Returns:
        str: A formatted string containing global news data
    """
    return route_to_vendor("get_global_news", curr_date, look_back_days, limit)

@tool
def get_insider_sentiment(
    ticker: Annotated[str, "ticker symbol for the company"],
    curr_date: Annotated[str, "current date you are trading at, yyyy-mm-dd"],
) -> str:
    """
    Retrieve insider sentiment information about a company.
    Uses the configured news_data vendor.
    Args:
        ticker (str): Ticker symbol of the company
        curr_date (str): Current date you are trading at, yyyy-mm-dd
    Returns:
        str: A report of insider sentiment data
    """
    return route_to_vendor("get_insider_sentiment", ticker, curr_date)

@tool
def get_insider_transactions(
    ticker: Annotated[str, "ticker symbol"],
    curr_date: Annotated[str, "current date you are trading at, yyyy-mm-dd"],
) -> str:
    """
    Retrieve insider transaction information about a company.
    Uses the configured news_data vendor.
    Args:
        ticker (str): Ticker symbol of the company
        curr_date (str): Current date you are trading at, yyyy-mm-dd
    Returns:
        str: A report of insider transaction data
    """
    return route_to_vendor("get_insider_transactions", ticker, curr_date)


@tool
def get_economic_calendar(
    start_date: Annotated[str, "Start date in YYYY-MM-DD format"] = None,
    end_date: Annotated[str, "End date in YYYY-MM-DD format"] = None,
    horizon: Annotated[str, "Time horizon: 3month, 6month, or 12month"] = "3month"
) -> str:
    """
    Retrieve upcoming economic events and market-moving catalysts.
    Provides critical context including FOMC meetings, GDP, CPI, employment data, earnings seasons.
    
    Args:
        start_date: Optional start date (default: today)
        end_date: Optional end date (default: based on horizon)
        horizon: Time window - "3month", "6month", or "12month" (default: 3month)
    
    Returns:
        Formatted report of upcoming high-impact economic events
    """
    from tradingagents.dataflows.alpha_vantage_economic import get_economic_calendar as get_econ_cal
    return get_econ_cal(start_date, end_date, horizon)


@tool
def get_upcoming_earnings(
    ticker: Annotated[str, "Stock ticker symbol"],
    horizon: Annotated[str, "Time horizon: 3month, 6month, or 12month"] = "3month"
) -> str:
    """
    Get upcoming earnings announcement dates for a specific ticker.
    Important for timing trades around volatility events.
    
    Args:
        ticker: Stock ticker symbol
        horizon: Time window - "3month", "6month", or "12month" (default: 3month)
    
    Returns:
        Report of upcoming earnings dates and estimates
    """
    from tradingagents.dataflows.alpha_vantage_economic import get_upcoming_earnings as get_earnings
    return get_earnings(ticker, horizon)
