import time
import json
from openai import BadRequestError


def create_research_manager(llm, memory):
    def research_manager_node(state) -> dict:
        history = state["investment_debate_state"].get("history", "")
        market_research_report = state["market_report"]
        sentiment_report = state["sentiment_report"]
        news_report = state["news_report"]
        fundamentals_report = state["fundamentals_report"]

        investment_debate_state = state["investment_debate_state"]

        curr_situation = f"{market_research_report}\n\n{sentiment_report}\n\n{news_report}\n\n{fundamentals_report}"
        past_memories = memory.get_memories(curr_situation, n_matches=2)

        past_memory_str = ""
        for i, rec in enumerate(past_memories, 1):
            past_memory_str += rec["recommendation"] + "\n\n"

        prompt = f"""As the portfolio manager and debate facilitator, your role is to critically evaluate this round of debate and make a definitive decision: align with the bear analyst, the bull analyst, or choose Hold only if it is strongly justified based on the arguments presented.

Summarize the key points from both sides concisely, focusing on the most compelling evidence or reasoning. Your recommendation—Buy, Sell, or Hold—must be clear and actionable. Avoid defaulting to Hold simply because both sides have valid points; commit to a stance grounded in the debate's strongest arguments.

Additionally, develop a detailed investment plan for the trader. This should include:

Your Recommendation: A decisive stance supported by the most convincing arguments.
Rationale: An explanation of why these arguments lead to your conclusion.
Strategic Actions: Concrete steps for implementing the recommendation.
Take into account your past mistakes on similar situations. Use these insights to refine your decision-making and ensure you are learning and improving. Present your analysis conversationally, as if speaking naturally, without special formatting. 

Here are your past reflections on mistakes:
\"{past_memory_str}\"

Here is the debate:
Debate History:
{history}"""

        try:
            from ..utils.rate_limiter import rate_limited
            
            @rate_limited(estimated_tokens=10000, cache_enabled=False)
            def _invoke_llm():
                return llm.invoke(prompt)
            
            response = _invoke_llm()
            response_content = response.content
        except BadRequestError as e:
            # Handle Azure content policy violations
            if "content management policy" in str(e).lower() or "content filtering" in str(e).lower():
                print(f"[WARNING] Content filtered by Azure OpenAI policy. Using fallback response.")
                response_content = """Based on the available research reports, I recommend a HOLD position.

**Rationale:**
The analysis was limited due to content filtering restrictions, but based on the available market data, technical indicators, and fundamental information, maintaining the current position appears prudent until more comprehensive analysis can be completed.

**Strategic Actions:**
1. Monitor key technical levels and volume patterns
2. Review fundamental metrics when additional data becomes available
3. Set appropriate stop-loss levels based on recent volatility
4. Re-evaluate position when market conditions stabilize

This recommendation prioritizes capital preservation while awaiting clearer market signals."""
            else:
                raise  # Re-raise if it's a different error

        new_investment_debate_state = {
            "judge_decision": response_content,
            "history": investment_debate_state.get("history", ""),
            "bear_history": investment_debate_state.get("bear_history", ""),
            "bull_history": investment_debate_state.get("bull_history", ""),
            "current_response": response_content,
            "count": investment_debate_state["count"],
        }

        return {
            "investment_debate_state": new_investment_debate_state,
            "investment_plan": response_content,
        }

    return research_manager_node
