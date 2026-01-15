"""
AI agent endpoints for natural language todo operations
"""

from fastapi import APIRouter, Depends, HTTPException, status
from app.api.deps import get_agent_service
from app.services.agent_service import AgentService
from app.domain.schemas import AgentRequest, AgentResponse
from app.utils.exceptions import AgentExecutionError

router = APIRouter(prefix="/agent", tags=["AI Agent"])


@router.post("/query", response_model=AgentResponse)
async def query_agent(
    request: AgentRequest,
    agent_service: AgentService = Depends(get_agent_service)
):
    """
    Send a natural language query to the AI agent
    
    Examples:
    - "Create a todo to buy groceries"
    - "Show me all my incomplete todos"
    - "Mark 'buy groceries' as complete"
    - "Delete the todo about laundry"
    """
    try:
        result = await agent_service.process_query(request.query)
        return AgentResponse(**result)
    except AgentExecutionError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}"
        )

