from datetime import datetime
from pydantic import BaseModel, Field
from app.domain.enums import TodoPriority


class TodoCreate(BaseModel):
    """Schema for creating a new todo"""
    title: str = Field(..., min_length=1, max_length=255)
    description: str | None = Field(None, max_length=2000)
    priority: TodoPriority = Field(default=TodoPriority.MEDIUM, description="Priority level")


class TodoUpdate(BaseModel):
    """Schema for updating an existing todo"""
    title: str | None = Field(None, min_length=1, max_length=255)
    description: str | None = Field(None, max_length=2000)
    completed: bool | None = None
    priority: TodoPriority | None = Field(None, description="Priority level")


class TodoRead(BaseModel):
    """Schema for reading a todo"""
    id: int
    title: str
    description: str | None
    completed: bool
    priority: TodoPriority
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class AgentRequest(BaseModel):
    """Schema for agent natural language requests"""
    query: str = Field(..., min_length=1, max_length=1000, description="Natural language query for the AI agent")


class UsageStats(BaseModel):
    """Token usage and cost statistics"""
    llm_calls: int = Field(0, description="Number of LLM API calls made")
    prompt_tokens: int = Field(0, description="Number of tokens in prompts")
    completion_tokens: int = Field(0, description="Number of tokens in completions")
    total_tokens: int = Field(0, description="Total tokens used")
    estimated_cost_usd: float = Field(0.0, description="Estimated cost in USD")
    model: str = Field("", description="Model used for generation")


class AgentResponse(BaseModel):
    """Schema for agent responses"""
    response: str
    actions_taken: list[str] = []
    usage: UsageStats = Field(default_factory=UsageStats, description="Token usage and cost statistics")

