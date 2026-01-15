"""
Agent executor setup and configuration
"""

from langchain.agents import AgentExecutor, initialize_agent, AgentType
from app.agents.todo_agent import create_llm
from app.utils.constants import AGENT_MAX_ITERATIONS


def build_agent_executor(tools):
    """
    Build an AgentExecutor with the provided tools
    
    Args:
        tools: List of LangChain tools
        
    Returns:
        AgentExecutor instance
    """
    llm = create_llm()
    
    # Use STRUCTURED_CHAT - compatible with OpenRouter's current API
    return initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        max_iterations=AGENT_MAX_ITERATIONS,
        handle_parsing_errors=True,
    )

