"""Callbacks for tracking LLM usage and costs"""

from typing import Any
from langchain.callbacks.base import BaseCallbackHandler
from langchain_core.outputs import LLMResult
from app.domain.schemas import UsageStats


# Pricing per 1M tokens (as of Jan 2026 - update as needed)
MODEL_PRICING = {
    # OpenAI models
    "openai/gpt-4o": {"prompt": 2.50, "completion": 10.00},
    "openai/gpt-4o-mini": {"prompt": 0.15, "completion": 0.60},
    "openai/gpt-4-turbo": {"prompt": 10.00, "completion": 30.00},
    "openai/gpt-3.5-turbo": {"prompt": 0.50, "completion": 1.50},
    
    # Anthropic models
    "anthropic/claude-3-opus": {"prompt": 15.00, "completion": 75.00},
    "anthropic/claude-3-sonnet": {"prompt": 3.00, "completion": 15.00},
    "anthropic/claude-3-haiku": {"prompt": 0.25, "completion": 1.25},
    
    # Meta Llama models
    "meta-llama/llama-3-70b-instruct": {"prompt": 0.80, "completion": 0.80},
    "meta-llama/llama-3-8b-instruct": {"prompt": 0.18, "completion": 0.18},
    
    # Google models
    "google/gemini-pro": {"prompt": 0.50, "completion": 1.50},
    "google/gemini-pro-1.5": {"prompt": 1.25, "completion": 5.00},
    
    # Mistral models
    "mistralai/mixtral-8x7b-instruct": {"prompt": 0.50, "completion": 0.50},
    "mistralai/mistral-large": {"prompt": 4.00, "completion": 12.00},
}


class TokenTrackingCallback(BaseCallbackHandler):
    """Callback handler to track token usage and costs"""
    
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.llm_calls = 0
        self.prompt_tokens = 0
        self.completion_tokens = 0
        self.total_tokens = 0
        
    def on_llm_start(self, serialized: dict[str, Any], prompts: list[str], **kwargs: Any) -> None:
        """Called when LLM starts running"""
        self.llm_calls += 1
    
    def on_llm_end(self, response: LLMResult, **kwargs: Any) -> None:
        """Called when LLM ends running - extract token usage"""
        if response.llm_output and "token_usage" in response.llm_output:
            usage = response.llm_output["token_usage"]
            self.prompt_tokens += usage.get("prompt_tokens", 0)
            self.completion_tokens += usage.get("completion_tokens", 0)
            self.total_tokens += usage.get("total_tokens", 0)
    
    def calculate_cost(self) -> float:
        """Calculate estimated cost in USD"""
        # Get pricing for the model (default to gpt-4o-mini if not found)
        pricing = MODEL_PRICING.get(
            self.model_name,
            MODEL_PRICING.get("openai/gpt-4o-mini", {"prompt": 0.15, "completion": 0.60})
        )
        
        # Calculate cost per million tokens
        prompt_cost = (self.prompt_tokens / 1_000_000) * pricing["prompt"]
        completion_cost = (self.completion_tokens / 1_000_000) * pricing["completion"]
        
        return prompt_cost + completion_cost
    
    def get_usage_stats(self) -> UsageStats:
        """Get usage statistics as a UsageStats object"""
        return UsageStats(
            llm_calls=self.llm_calls,
            prompt_tokens=self.prompt_tokens,
            completion_tokens=self.completion_tokens,
            total_tokens=self.total_tokens,
            estimated_cost_usd=round(self.calculate_cost(), 6),
            model=self.model_name
        )


