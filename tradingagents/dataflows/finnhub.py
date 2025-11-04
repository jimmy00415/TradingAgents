"""
Finnhub API Integration
Provides institutional-grade financial data including insider sentiment,
earnings surprises, and institutional ownership data.
"""
import os
from typing import Annotated
from datetime import datetime, timedelta
import finnhub


def _get_finnhub_client():
    """Get configured Finnhub client instance."""
    api_key = os.getenv("FINNHUB_API_KEY")
    if not api_key or api_key == "your_finnhub_api_key_here":
        raise ValueError(
            "Finnhub API key not configured. "
            "Please set FINNHUB_API_KEY in your .env file. "
            "Get a free key at: https://finnhub.io/register"
        )
    return finnhub.Client(api_key=api_key)


def get_company_news_finnhub(
    ticker: Annotated[str, "Stock ticker symbol"],
    start_date: Annotated[str, "Start date in YYYY-MM-DD format"],
    end_date: Annotated[str, "End date in YYYY-MM-DD format"]
) -> str:
    """
    Retrieve company-specific news from Finnhub.
    
    Args:
        ticker: Stock ticker symbol
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
    
    Returns:
        Formatted string with news articles
    """
    try:
        client = _get_finnhub_client()
        
        # Finnhub expects dates in YYYY-MM-DD format (already provided)
        news = client.company_news(ticker, _from=start_date, to=end_date)
        
        if not news:
            return f"No Finnhub news found for {ticker} between {start_date} and {end_date}."
        
        # Format news into readable report
        report = [
            f"## Finnhub Company News for {ticker}",
            f"**Period**: {start_date} to {end_date}",
            f"**Total Articles**: {len(news)}\n"
        ]
        
        for article in news[:20]:  # Limit to top 20 articles
            headline = article.get('headline', 'No headline')
            summary = article.get('summary', '')
            source = article.get('source', 'Unknown')
            url = article.get('url', '')
            datetime_unix = article.get('datetime', 0)
            
            # Convert Unix timestamp to readable date
            if datetime_unix:
                article_date = datetime.fromtimestamp(datetime_unix).strftime('%Y-%m-%d %H:%M')
            else:
                article_date = 'Unknown date'
            
            report.append(f"### {headline}")
            report.append(f"**Date**: {article_date} | **Source**: {source}")
            if summary:
                report.append(f"{summary[:300]}..." if len(summary) > 300 else summary)
            if url:
                report.append(f"[Read more]({url})")
            report.append("")  # Blank line
        
        return "\n".join(report)
    
    except Exception as e:
        print(f"[INFO] Finnhub news unavailable: {e}")
        return f"Finnhub news data not available for {ticker}."


def get_insider_sentiment_finnhub(
    ticker: Annotated[str, "Stock ticker symbol"],
    start_date: Annotated[str, "Start date in YYYY-MM-DD format"],
    end_date: Annotated[str, "End date in YYYY-MM-DD format"]
) -> str:
    """
    Retrieve aggregated insider sentiment data from Finnhub.
    
    This provides monthly aggregated insider trading statistics including:
    - Net change in shares (buying vs selling)
    - Number of transactions
    - MSPR (Monthly Share Purchase Ratio)
    
    Args:
        ticker: Stock ticker symbol
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
    
    Returns:
        Formatted report of insider sentiment trends
    """
    try:
        client = _get_finnhub_client()
        
        sentiment = client.stock_insider_sentiment(ticker, _from=start_date, to=end_date)
        
        if not sentiment or 'data' not in sentiment or not sentiment['data']:
            return f"No insider sentiment data available for {ticker}."
        
        data = sentiment['data']
        symbol = sentiment.get('symbol', ticker)
        
        report = [
            f"## Finnhub Insider Sentiment for {symbol}",
            f"**Period**: {start_date} to {end_date}",
            f"**Data Points**: {len(data)}\n",
            "### Monthly Insider Activity\n"
        ]
        
        for entry in data:
            year = entry.get('year', 'N/A')
            month = entry.get('month', 'N/A')
            change = entry.get('change', 0)
            mspr = entry.get('mspr', 0)
            
            # Interpret the data
            sentiment_label = "🟢 BULLISH" if change > 0 else "🔴 BEARISH" if change < 0 else "⚪ NEUTRAL"
            
            report.append(f"**{year}-{month:02d}** | {sentiment_label}")
            report.append(f"- Net Share Change: {change:,} shares")
            report.append(f"- MSPR (Monthly Share Purchase Ratio): {mspr:.2f}")
            report.append("")
        
        # Add interpretation guide
        report.append("\n### Interpretation Guide:")
        report.append("- **Positive Net Change**: Insiders buying more than selling (bullish signal)")
        report.append("- **Negative Net Change**: Insiders selling more than buying (bearish signal)")
        report.append("- **MSPR > 0**: More purchases than sales")
        report.append("- **MSPR < 0**: More sales than purchases")
        
        return "\n".join(report)
    
    except Exception as e:
        print(f"[INFO] Finnhub insider sentiment unavailable: {e}")
        return f"Finnhub insider sentiment data not available for {ticker}."


def get_insider_transactions_finnhub(
    ticker: Annotated[str, "Stock ticker symbol"]
) -> str:
    """
    Retrieve individual insider transactions from Finnhub.
    
    Shows specific insider trades with names, positions, and transaction details.
    
    Args:
        ticker: Stock ticker symbol
    
    Returns:
        Formatted report of recent insider transactions
    """
    try:
        client = _get_finnhub_client()
        
        transactions = client.stock_insider_transactions(ticker)
        
        if not transactions or 'data' not in transactions or not transactions['data']:
            return f"No insider transactions available for {ticker}."
        
        data = transactions['data']
        symbol = transactions.get('symbol', ticker)
        
        report = [
            f"## Finnhub Insider Transactions for {symbol}",
            f"**Recent Transactions**: {len(data)}\n"
        ]
        
        for txn in data[:15]:  # Limit to 15 most recent
            name = txn.get('name', 'Unknown')
            share = txn.get('share', 0)
            change = txn.get('change', 0)
            filing_date = txn.get('filingDate', 'N/A')
            transaction_date = txn.get('transactionDate', 'N/A')
            transaction_code = txn.get('transactionCode', '')
            
            # Determine transaction type
            if change > 0:
                action = "🟢 BUY"
            elif change < 0:
                action = "🔴 SELL"
            else:
                action = "⚪ OTHER"
            
            report.append(f"### {action} - {name}")
            report.append(f"- **Transaction Date**: {transaction_date}")
            report.append(f"- **Filing Date**: {filing_date}")
            report.append(f"- **Shares Changed**: {change:,}")
            report.append(f"- **Total Shares After**: {share:,}")
            if transaction_code:
                report.append(f"- **Transaction Code**: {transaction_code}")
            report.append("")
        
        return "\n".join(report)
    
    except Exception as e:
        print(f"[INFO] Finnhub insider transactions unavailable: {e}")
        return f"Finnhub insider transaction data not available for {ticker}."


def get_earnings_surprises_finnhub(
    ticker: Annotated[str, "Stock ticker symbol"],
    limit: Annotated[int, "Number of quarters to retrieve"] = 4
) -> str:
    """
    Retrieve earnings surprise data from Finnhub.
    
    Shows historical earnings performance vs. analyst estimates.
    
    Args:
        ticker: Stock ticker symbol
        limit: Number of recent quarters to show (default: 4)
    
    Returns:
        Formatted report of earnings surprises
    """
    try:
        client = _get_finnhub_client()
        
        surprises = client.company_earnings(ticker, limit=limit)
        
        if not surprises:
            return f"No earnings surprise data available for {ticker}."
        
        report = [
            f"## Finnhub Earnings Surprises for {ticker}",
            f"**Quarters Analyzed**: {len(surprises)}\n"
        ]
        
        for earnings in surprises:
            period = earnings.get('period', 'N/A')
            actual = earnings.get('actual', 0)
            estimate = earnings.get('estimate', 0)
            surprise = earnings.get('surprise', 0)
            surprise_percent = earnings.get('surprisePercent', 0)
            
            # Determine beat/miss
            if surprise > 0:
                result = "🟢 BEAT"
            elif surprise < 0:
                result = "🔴 MISS"
            else:
                result = "⚪ IN-LINE"
            
            report.append(f"### {period} - {result}")
            report.append(f"- **Actual EPS**: ${actual:.2f}")
            report.append(f"- **Estimate**: ${estimate:.2f}")
            report.append(f"- **Surprise**: ${surprise:.2f} ({surprise_percent:.1f}%)")
            report.append("")
        
        report.append("\n### Trading Implications:")
        report.append("- Consistent beats suggest strong execution and pricing power")
        report.append("- Misses may indicate operational challenges or market headwinds")
        report.append("- Large surprises (>10%) often trigger significant stock moves")
        
        return "\n".join(report)
    
    except Exception as e:
        print(f"[INFO] Finnhub earnings surprises unavailable: {e}")
        return f"Finnhub earnings data not available for {ticker}."


def get_institutional_ownership_finnhub(
    ticker: Annotated[str, "Stock ticker symbol"]
) -> str:
    """
    Retrieve institutional ownership data from Finnhub.
    
    Shows which institutions hold the stock and their position sizes.
    
    Args:
        ticker: Stock ticker symbol
    
    Returns:
        Formatted report of institutional ownership
    """
    try:
        client = _get_finnhub_client()
        
        ownership = client.institutional_ownership(ticker)
        
        if not ownership or 'data' not in ownership or not ownership['data']:
            return f"No institutional ownership data available for {ticker}."
        
        data = ownership['data']
        symbol = ownership.get('symbol', ticker)
        
        report = [
            f"## Finnhub Institutional Ownership for {symbol}",
            f"**Number of Institutions**: {len(data)}\n",
            "### Top Institutional Holders\n"
        ]
        
        for holder in data[:20]:  # Top 20 institutions
            name = holder.get('name', 'Unknown')
            share = holder.get('share', 0)
            change = holder.get('change', 0)
            filing_date = holder.get('filingDate', 'N/A')
            
            change_label = ""
            if change > 0:
                change_label = f" 🟢 (+{change:,} shares)"
            elif change < 0:
                change_label = f" 🔴 ({change:,} shares)"
            
            report.append(f"**{name}**{change_label}")
            report.append(f"- Holdings: {share:,} shares")
            report.append(f"- Last Filing: {filing_date}")
            report.append("")
        
        return "\n".join(report)
    
    except Exception as e:
        print(f"[INFO] Finnhub institutional ownership unavailable: {e}")
        return f"Finnhub institutional ownership data not available for {ticker}."
