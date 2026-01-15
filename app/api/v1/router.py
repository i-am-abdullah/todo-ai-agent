"""
API v1 router aggregator
"""

from fastapi import APIRouter
from app.api.v1 import todos, agent

api_router = APIRouter()

# Include all v1 routers
api_router.include_router(todos.router)
api_router.include_router(agent.router)

