"""
Base abstractions for LangChain tools

This module provides base classes and utilities for creating
custom LangChain tools with proper error handling and logging.
"""

from typing import Any
from app.core.logging import get_logger

logger = get_logger(__name__)


def format_tool_response(success: bool, message: str, data: Any = None) -> str:
    """
    Format a consistent tool response
    
    Args:
        success: Whether the operation was successful
        message: Human-readable message
        data: Optional data to include
    
    Returns:
        Formatted string response
    """
    if success:
        response = f"✓ {message}"
        if data:
            response += f"\n{data}"
        return response
    else:
        return f"✗ {message}"

