from enum import Enum


class TodoStatus(str, Enum):
    """
    Todo completion status
    
    Note: Currently not used in favor of boolean 'completed' field.
    Kept for future enhancement where todos might have more states:
    - pending, in_progress, completed, archived, etc.
    """
    PENDING = "pending"
    COMPLETED = "completed"


class TodoPriority(str, Enum):
    """
    Todo priority levels
    
    Used to categorize todos by importance:
    - low: Nice to have, no urgency
    - medium: Normal priority (default)
    - high: Important, should be done soon
    - urgent: Critical, needs immediate attention
    """
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

