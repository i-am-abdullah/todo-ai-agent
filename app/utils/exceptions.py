class TodoNotFoundError(Exception):
    """Raised when a todo item is not found"""
    pass


class TodoAlreadyExistsError(Exception):
    """Raised when attempting to create a duplicate todo"""
    pass


class AgentExecutionError(Exception):
    """Raised when agent execution fails"""
    pass

