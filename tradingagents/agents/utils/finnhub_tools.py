"""
Finnhub-specific advanced tools for institutional-grade analysis.
These tools provide data beyond standard fundamentals.
"""
from langchain_core.tools import tool
from typing import Annotated


@tool
def get_earnings_surprises(
    ticker: Annotated[str, "Stock ticker symbol"],
    limit: Annotated[int, "Number of quarters to analyze"] = 4
) -> str:
    """
    Retrieve earnings surprise data showing actual vs estimated EPS.
    
    Critical for assessing:
    - Management execution quality (consistent beats = strong)
    - Analyst confidence and estimate accuracy
    - Post-earnings stock reaction patterns
    
    Args:
        ticker: Stock ticker symbol
        limit: Number of recent quarters (default: 4)
    
    Returns:
        Report of earnings beats/misses with percentages
    """
    from tradingagents.dataflows.finnhub import get_earnings_surprises_finnhub
    return get_earnings_surprises_finnhub(ticker, limit)


@tool
def get_institutional_ownership(
    ticker: Annotated[str, "Stock ticker symbol"]
) -> str:
    """
    Retrieve institutional ownership data showing which major institutions hold the stock.
    
    Key insights:
    - Smart money positioning (hedge funds, mutual funds)
    - Recent changes in institutional holdings
    - Institutional conviction levels
    
    Args:
        ticker: Stock ticker symbol
    
    Returns:
        Report of top institutional holders and their position changes
    """
    from tradingagents.dataflows.finnhub import get_institutional_ownership_finnhub
    return get_institutional_ownership_finnhub(ticker)
