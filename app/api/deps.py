"""
Dependency injection for API routes
"""

from functools import lru_cache
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.repositories.todo_repository import TodoRepository
from app.services.todo_service import TodoService
from app.services.agent_service import AgentService
from app.tools.todo_tools import build_todo_tools
from app.agents.executor import build_agent_executor


def get_todo_service(db: AsyncSession = Depends(get_db)) -> TodoService:
    """Dependency for getting TodoService"""
    repo = TodoRepository(db)
    return TodoService(repo)


@lru_cache
def get_agent_executor_cached():
    """
    Get a cached agent executor (without DB dependencies)
    This is cached because the LLM and agent setup is expensive
    """
    # Note: Tools will be built with service in the endpoint
    # This just creates the executor structure
    return None


async def get_agent_service(
    todo_service: TodoService = Depends(get_todo_service)
) -> AgentService:
    """
    Dependency for getting AgentService with tools
    
    Note: This creates a new agent executor for each request with the
    current database session's TodoService
    """
    tools = build_todo_tools(todo_service)
    agent_executor = build_agent_executor(tools)
    return AgentService(agent_executor)

