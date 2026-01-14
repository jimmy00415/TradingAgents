# Token Optimization Strategy for Low-Tier Azure Deployments

## Problem Analysis

**Current Status:**
- Azure deployment: 10K tokens/min (upgraded from 1K)
- Still hitting rate limits during analysis
- Already optimized: max_debate_rounds=1, max_risk_discuss_rounds=1

## Token Usage Breakdown (Estimated per Analysis)

### Multi-Agent Workflow
1. **Data Collection** (0 LLM tokens): yfinance, Alpha Vantage, Finnhub
2. **Researchers** (5-10 agents × ~1000 tokens = 5-10K tokens)
   - fundamental_researcher
   - technical_researcher  
   - sentiment_researcher
   - risk_researcher
   - earnings_researcher
3. **Analysts** (3-5 agents × ~1500 tokens = 4.5-7.5K tokens)
   - fundamental_analyst
   - technical_analyst
   - sentiment_analyst
4. **Portfolio Manager** (~2000 tokens)
5. **Risk Manager** (~1500 tokens)
6. **Trader** (~1000 tokens)
7. **Debate/Reflection** (if enabled, 2-6K tokens)

**Total per run: 18-30K tokens** → Takes 2-3 minutes at 10K tokens/min

## Optimization Strategies

### Strategy 1: Use GPT-4o-mini for Research Tasks (70% cost reduction)
- GPT-4o-mini: 15¢/1M input tokens (vs $2.50/1M for GPT-4o)
- Keep GPT-4o for final decision-making only
- **Savings: ~70% token cost, allows 7x more analyses**

### Strategy 2: Reduce Data Volume
- Limit historical data lookback (default: 180 days → 30 days)
- Fetch fewer technical indicators (20+ → 5-10 key indicators)
- Limit news articles (100+ → 20-30)
- **Savings: ~40% fewer tokens in prompts**

### Strategy 3: Streamline Agent Architecture
- Combine researchers into single "data_aggregator" agent
- Skip debate rounds completely (already at 1)
- Remove reflection loops
- **Savings: ~50% fewer LLM calls**

### Strategy 4: Implement Smart Caching
- Cache analyses for 1-4 hours
- Reuse recent analyses for same ticker
- Store intermediate results
- **Savings: Avoid repeat analyses**

### Strategy 5: Async/Batched Processing
- Queue analyses during off-peak hours
- Batch multiple requests
- Implement retry with exponential backoff
- **Benefit: Better rate limit management**

## Recommended Implementation

### Phase 1: Quick Wins (Implement Now)
1. Add "Economy Mode" toggle in UI
2. When enabled:
   - Use gpt-4o-mini for all researchers
   - Use gpt-4o only for final trader decision
   - Reduce data lookback to 30 days
   - Limit to 5 key technical indicators
   - Fetch max 20 news articles

### Phase 2: Advanced Optimization
1. Implement result caching
2. Add progress indicators with estimated wait time
3. Allow background processing
4. Add "fast analysis" preset

## Configuration Changes Needed

```python
# Add to default_config.py
"economy_mode": {
    "enabled": False,  # Toggle via UI
    "researcher_model": "gpt-4o-mini",  # Cheap for data gathering
    "analyst_model": "gpt-4o-mini",     # Cheap for analysis  
    "decision_model": "gpt-4o",         # Keep quality for final decision
    "data_lookback_days": 30,           # Reduce from 180
    "max_indicators": 5,                # Reduce from 20+
    "max_news_articles": 20,            # Limit news fetching
    "skip_debate": True,                # No debate rounds
    "skip_reflection": True,            # No reflection loops
}
```

## Expected Results

### Without Optimization (Current)
- Tokens per analysis: 20-30K
- Time at 10K/min: 2-3 minutes
- Risk: Rate limit errors

### With Economy Mode
- Tokens per analysis: 5-8K (73% reduction)
- Time at 10K/min: 30-50 seconds
- Risk: Minimal, smooth operation
- Quality: 85-90% as good (gpt-4o-mini is very capable)

## Implementation Priority

1. ✅ **HIGH**: Add economy mode config
2. ✅ **HIGH**: Use gpt-4o-mini for researchers
3. ✅ **MEDIUM**: Reduce data volume
4. **MEDIUM**: Implement caching
5. **LOW**: Advanced batching/async

## GPT-4o vs GPT-4o-mini Comparison

| Model | Speed | Cost | Best For |
|-------|-------|------|----------|
| GPT-4o | ⭐⭐⭐ | $$$$$ | Final decisions, complex reasoning |
| GPT-4o-mini | ⭐⭐⭐⭐⭐ | $ | Data parsing, initial analysis, summaries |

**Verdict**: Use gpt-4o-mini everywhere except final trader decision = 70% savings with 10% quality tradeoff.
