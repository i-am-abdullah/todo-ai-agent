"""
Tool configuration, metadata, and safety rules
"""

# Tool descriptions for the agent
TOOL_DESCRIPTIONS = {
    "create_todo": """
    Create a new todo item.
    Use this when the user wants to add a new task or todo.
    Required: title (what needs to be done)
    Optional: description (additional details)
    """,
    
    "list_todos": """
    List all todo items.
    Use this when the user wants to see all their todos or tasks.
    """,
    
    "get_completed_todos": """
    Get todos filtered by completion status.
    Use this when the user asks for completed or incomplete todos.
    Required: completed (true for completed, false for incomplete)
    """,
    
    "update_todo": """
    Update an existing todo item.
    Use this when the user wants to modify, edit, or change a todo.
    Required: text (identifier to find the todo)
    Optional: title, description, completed (fields to update)
    """,
    
    "delete_todo": """
    Delete a todo item.
    Use this when the user wants to remove or delete a todo.
    Required: text (identifier to find the todo)
    """,
    
    "mark_complete": """
    Mark a todo as completed.
    Use this when the user wants to complete or finish a todo.
    Required: text (identifier to find the todo)
    """,
    
    "mark_incomplete": """
    Mark a todo as incomplete.
    Use this when the user wants to reopen or uncomplete a todo.
    Required: text (identifier to find the todo)
    """,
}

# Safety rules
SAFETY_RULES = [
    "Always confirm destructive operations (delete, clear all)",
    "Provide clear feedback about what was changed",
    "Handle errors gracefully with helpful messages",
]

