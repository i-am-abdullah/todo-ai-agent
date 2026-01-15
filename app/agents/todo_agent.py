"""
LangChain AI agent configuration for todo operations
"""

from langchain_community.chat_models import ChatOpenAI
from app.core.config import get_settings
from app.agents.prompts import SYSTEM_PROMPT

settings = get_settings()


def create_llm():
    """Create and configure the LLM for the agent"""
    return ChatOpenAI(
        api_key=settings.OPENROUTER_API_KEY,
        base_url="https://openrouter.ai/api/v1",
        model=settings.OPENROUTER_MODEL,
        temperature=0.7,
        model_kwargs={
            "extra_body": {
                "system": SYSTEM_PROMPT,
            }
        }
    )

