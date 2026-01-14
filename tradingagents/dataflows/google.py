from typing import Annotated
from datetime import datetime
from dateutil.relativedelta import relativedelta
from .googlenews_utils import getNewsData


def get_google_news(
    query: Annotated[str, "Query to search with"],
    curr_date: Annotated[str, "Curr date in yyyy-mm-dd format"],
    look_back_days: Annotated[int, "how many days to look back"],
) -> str:
    """Get Google News with (query, curr_date, look_back_days) parameters."""
    # Type safety: ensure parameters are correct types
    query = str(query).replace(" ", "+")
    curr_date = str(curr_date)  # Ensure curr_date is string
    look_back_days = int(look_back_days)  # Ensure int

    try:
        start_date = datetime.strptime(curr_date, "%Y-%m-%d")
    except ValueError as e:
        print(f"[ERROR] Invalid date format for curr_date='{curr_date}': {e}")
        return ""
    
    before = start_date - relativedelta(days=look_back_days)
    before = before.strftime("%Y-%m-%d")

    try:
        news_results = getNewsData(query, before, curr_date)
    except Exception as e:
        print(f"[ERROR] Google News scraping failed: {e}")
        return ""

    news_str = ""

    for news in news_results:
        try:
            news_str += (
                f"### {news['title']} (source: {news['source']}) \n\n{news['snippet']}\n\n"
            )
        except (KeyError, TypeError) as e:
            print(f"[WARNING] Skipping malformed news item: {e}")
            continue

    if len(news_results) == 0:
        return ""

    return f"## {query} Google News, from {before} to {curr_date}:\n\n{news_str}"


def get_google_company_news(
    ticker: Annotated[str, "Ticker symbol"],
    start_date: Annotated[str, "Start date in yyyy-mm-dd format"],
    end_date: Annotated[str, "End date in yyyy-mm-dd format"],
) -> str:
    """Adapter for get_news signature: converts (ticker, start_date, end_date) to Google News format."""
    # Calculate look_back_days from date range
    start_dt = datetime.strptime(start_date, "%Y-%m-%d")
    end_dt = datetime.strptime(end_date, "%Y-%m-%d")
    look_back_days = (end_dt - start_dt).days
    
    # Use end_date as curr_date and calculate backwards
    return get_google_news(ticker, end_date, look_back_days)