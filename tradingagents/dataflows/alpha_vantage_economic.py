"""
Alpha Vantage Economic Calendar Integration
Provides macroeconomic event tracking for context-aware trading analysis
"""
from typing import Annotated
from datetime import datetime, timedelta
from .alpha_vantage_common import make_alpha_vantage_request


def get_economic_calendar(
    start_date: Annotated[str, "Start date in YYYY-MM-DD format"] = None,
    end_date: Annotated[str, "End date in YYYY-MM-DD format"] = None,
    horizon: Annotated[str, "Time horizon: 3month, 6month, or 12month"] = "3month"
) -> str:
    """
    Retrieve upcoming economic events and indicators from Alpha Vantage Economic Calendar.
    
    This provides critical context for trading decisions by identifying:
    - FOMC meetings and Fed announcements
    - GDP releases
    - CPI/inflation reports  
    - Employment data (NFP, unemployment)
    - Earnings seasons
    - Other major economic events
    
    Args:
        start_date: Optional start date (default: today)
        end_date: Optional end date (default: based on horizon)
        horizon: Time window - "3month", "6month", or "12month" (default: 3month)
    
    Returns:
        Formatted string with upcoming economic events and their importance
    """
    # Build parameters
    params = {
        "function": "ECONOMIC_CALENDAR"
    }
    
    # Add horizon if no specific dates provided
    if not start_date and not end_date:
        params["horizon"] = horizon
    else:
        # Use specific date range if provided
        if start_date:
            params["from"] = start_date
        if end_date:
            params["to"] = end_date
    
    try:
        data = make_alpha_vantage_request(params)
        
        # Check if we got valid data
        if not data or "data" not in data:
            return "Economic calendar data not available at this time."
        
        events = data.get("data", [])
        
        if not events:
            return f"No economic events scheduled for the specified period."
        
        # Format the economic calendar into a readable report
        report_lines = [
            "## Upcoming Economic Events & Market-Moving Catalysts\n",
            f"**Period**: {start_date or 'Today'} to {end_date or f'Next {horizon}'}\n",
            f"**Total Events**: {len(events)}\n",
            "\n### High-Impact Events\n"
        ]
        
        high_impact = []
        medium_impact = []
        
        for event in events:
            event_date = event.get("date", "N/A")
            event_time = event.get("time", "")
            country = event.get("country", "")
            event_name = event.get("event", "Unknown Event")
            currency = event.get("currency", "")
            importance = event.get("importance", "").lower()
            actual = event.get("actual", "")
            previous = event.get("previous", "")
            estimate = event.get("estimate", "")
            
            # Build event description
            event_desc = f"**{event_date}** {event_time} - {country} - **{event_name}**"
            if currency:
                event_desc += f" ({currency})"
            
            details = []
            if estimate:
                details.append(f"Est: {estimate}")
            if previous:
                details.append(f"Prev: {previous}")
            if actual:
                details.append(f"Actual: {actual}")
            
            if details:
                event_desc += f" - {', '.join(details)}"
            
            # Categorize by importance
            if importance in ["high", "critical", "3"]:
                high_impact.append(event_desc)
            elif importance in ["medium", "moderate", "2"]:
                medium_impact.append(event_desc)
        
        # Add high-impact events
        if high_impact:
            for event in high_impact[:15]:  # Limit to top 15 high-impact
                report_lines.append(f"- {event}")
        else:
            report_lines.append("- No high-impact events identified")
        
        # Add medium-impact events
        if medium_impact:
            report_lines.append("\n### Medium-Impact Events\n")
            for event in medium_impact[:10]:  # Limit to top 10 medium-impact
                report_lines.append(f"- {event}")
        
        # Add trading implications
        report_lines.append("\n### Trading Implications\n")
        report_lines.append("**Key Considerations:**")
        report_lines.append("- High-impact events (FOMC, NFP, CPI) can cause 1-3% intraday moves in major indices")
        report_lines.append("- Avoid large positions immediately before major announcements unless hedged")
        report_lines.append("- Volatility typically increases 24-48 hours before scheduled events")
        report_lines.append("- Post-event volatility can create short-term trading opportunities")
        report_lines.append("- Compare actual vs. estimate - large surprises drive strongest reactions")
        
        return "\n".join(report_lines)
    
    except Exception as e:
        # Graceful degradation if economic calendar unavailable
        print(f"[INFO] Economic calendar unavailable: {e}")
        return f"Economic calendar data could not be retrieved. This is optional context and does not affect core analysis. Proceed with fundamental and technical analysis as usual."


def get_upcoming_earnings(
    ticker: Annotated[str, "Stock ticker symbol"],
    horizon: Annotated[str, "Time horizon: 3month, 6month, or 12month"] = "3month"
) -> str:
    """
    Get upcoming earnings announcement dates for a specific ticker.
    
    Note: This uses the earnings calendar function from Alpha Vantage.
    """
    params = {
        "function": "EARNINGS_CALENDAR",
        "symbol": ticker.upper(),
        "horizon": horizon
    }
    
    try:
        data = make_alpha_vantage_request(params)
        
        if not data:
            return f"Earnings calendar data not available for {ticker}."
        
        # Parse CSV response (Alpha Vantage returns CSV for earnings calendar)
        if isinstance(data, str):
            lines = data.strip().split('\n')
            if len(lines) <= 1:
                return f"No upcoming earnings found for {ticker}."
            
            # Parse header and data
            header = lines[0].split(',')
            earnings_data = []
            
            for line in lines[1:]:
                values = line.split(',')
                if len(values) >= 3:
                    earnings_data.append({
                        'symbol': values[0] if len(values) > 0 else '',
                        'name': values[1] if len(values) > 1 else '',
                        'reportDate': values[2] if len(values) > 2 else '',
                        'fiscalDateEnding': values[3] if len(values) > 3 else '',
                        'estimate': values[4] if len(values) > 4 else '',
                        'currency': values[5] if len(values) > 5 else ''
                    })
            
            if not earnings_data:
                return f"No upcoming earnings announcements found for {ticker}."
            
            report = [
                f"## Upcoming Earnings for {ticker}\n",
                f"**Horizon**: {horizon}\n",
                "**Scheduled Announcements:**\n"
            ]
            
            for earnings in earnings_data[:5]:  # Limit to next 5 earnings
                report.append(f"- **{earnings['reportDate']}** - Fiscal Period: {earnings['fiscalDateEnding']}")
                if earnings['estimate']:
                    report.append(f"  - EPS Estimate: {earnings['estimate']}")
            
            report.append("\n**Trading Notes:**")
            report.append("- Volatility typically increases 3-5 days before earnings")
            report.append("- Options implied volatility (IV) peaks just before announcement")
            report.append("- Historical earnings reactions can guide position sizing")
            
            return "\n".join(report)
    
    except Exception as e:
        print(f"[INFO] Earnings calendar unavailable for {ticker}: {e}")
        return f"Earnings calendar data not available for {ticker}. This does not affect core analysis."
