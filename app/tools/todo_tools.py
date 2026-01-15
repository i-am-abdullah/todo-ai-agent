"""
LangChain tools for todo operations
"""

from langchain_core.tools import tool
from app.services.todo_service import TodoService
from app.domain.schemas import TodoCreate, TodoUpdate
from app.domain.enums import TodoPriority
from app.tools.base import format_tool_response


# Constants
PAGE_SIZE = 20


# Helper functions for reusability
def get_priority_icon(priority_value: str) -> str:
    """Get emoji icon for priority level"""
    return {
        "low": "🔵",
        "medium": "🟡",
        "high": "🟠",
        "urgent": "🔴"
    }.get(priority_value, "⚪")


def validate_priority(priority: str) -> TodoPriority | None:
    """Validate and convert priority string to enum"""
    try:
        return TodoPriority(priority.lower())
    except ValueError:
        return None


def format_todo_line(todo, show_status: bool = True, show_priority: bool = True) -> str:
    """Format a single todo line with consistent styling"""
    parts = []
    
    if show_status:
        parts.append("✓" if todo.completed else "○")
    
    if show_priority:
        parts.append(get_priority_icon(todo.priority.value))
    
    parts.append(f"[{todo.id}] {todo.title}")
    
    if todo.description:
        parts.append(f"- {todo.description}")
    
    return " ".join(parts)


def format_todo_list(todos: list, show_status: bool = True, page: int = 1) -> str:
    """Format a list of todos with pagination support"""
    if not todos:
        return "No todos found"
    
    total = len(todos)
    start_idx = (page - 1) * PAGE_SIZE
    end_idx = start_idx + PAGE_SIZE
    page_todos = todos[start_idx:end_idx]
    
    lines = [f"Found {total} todo(s) (showing {len(page_todos)}):"]
    
    for todo in page_todos:
        lines.append(format_todo_line(todo, show_status=show_status))
    
    # Add pagination info if there are more todos
    if end_idx < total:
        remaining = total - end_idx
        lines.append(f"\n📄 {remaining} more todo(s) available. Say 'load more' or 'next page' to see them.")
    
    return "\n".join(lines)


def build_todo_tools(service: TodoService):
    """
    Build LangChain tools with access to TodoService
    
    Args:
        service: TodoService instance for performing operations
        
    Returns:
        List of LangChain tools
    """

    @tool
    async def create_todo(title: str, description: str | None = None, priority: str = "medium") -> str:
        """Create a new todo item. Provide a title, optional description, and priority (low, medium, high, urgent)."""
        try:
            # Validate priority
            priority_enum = validate_priority(priority)
            if not priority_enum:
                priority_enum = TodoPriority.MEDIUM
            
            # Check for duplicates
            existing = await service.find_by_text(title)
            if existing and existing.title.lower() == title.lower():
                return format_tool_response(
                    False,
                    f"Todo with similar title already exists: '{existing.title}' (ID: {existing.id})",
                    "Use update or choose a different title"
                )
            
            # Create new todo
            todo = await service.create_todo(
                TodoCreate(title=title, description=description, priority=priority_enum)
            )
            return format_tool_response(
                True,
                f"Created todo: '{todo.title}' [Priority: {todo.priority.value}]",
                f"ID: {todo.id}"
            )
        except Exception as e:
            return format_tool_response(False, f"Failed to create todo: {str(e)}")

    @tool
    async def list_todos(page: int = 1) -> str:
        """List all todo items with pagination (20 per page). Use page parameter to navigate: page=1, page=2, etc."""
        try:
            todos = await service.list_todos()
            if not todos:
                return format_tool_response(True, "No todos found")
            
            return format_todo_list(todos, show_status=True, page=page)
        except Exception as e:
            return format_tool_response(False, f"Failed to list todos: {str(e)}")

    @tool
    async def get_completed_todos(completed: bool, page: int = 1) -> str:
        """Get todos filtered by completion status with pagination. Set completed=True for completed todos, False for incomplete."""
        try:
            todos = await service.get_by_completed(completed)
            status_text = "completed" if completed else "incomplete"
            
            if not todos:
                return format_tool_response(True, f"No {status_text} todos found")
            
            return format_todo_list(todos, show_status=False, page=page)
        except Exception as e:
            return format_tool_response(False, f"Failed to get todos: {str(e)}")

    @tool
    async def update_todo(
        text: str,
        title: str | None = None,
        description: str | None = None,
        completed: bool | None = None,
        priority: str | None = None
    ) -> str:
        """Update a todo by matching its title or description. Provide the text to find the todo and fields to update. Priority can be: low, medium, high, urgent."""
        try:
            # Find the todo to update
            current_todo = await service.find_by_text(text)
            if not current_todo:
                return format_tool_response(False, f"Todo not found matching: '{text}'")
            
            # Validate priority if provided
            priority_enum = None
            if priority:
                priority_enum = validate_priority(priority)
                if not priority_enum:
                    return format_tool_response(False, f"Invalid priority '{priority}'. Use: low, medium, high, urgent")
            
            # Check for duplicate if title is being changed
            if title and title.lower() != current_todo.title.lower():
                existing = await service.find_by_text(title)
                if existing and existing.id != current_todo.id and existing.title.lower() == title.lower():
                    return format_tool_response(
                        False,
                        f"Another todo with title '{existing.title}' already exists (ID: {existing.id})",
                        f"Current todo: '{current_todo.title}' (ID: {current_todo.id})\n"
                        f"Do you want to:\n"
                        f"1. Update existing '{existing.title}' instead?\n"
                        f"2. Choose a different title for '{current_todo.title}'?\n"
                        f"3. Merge them by deleting one?"
                    )
            
            # Proceed with update
            todo = await service.update_by_text(
                text,
                TodoUpdate(title=title, description=description, completed=completed, priority=priority_enum)
            )
            
            return format_tool_response(
                True,
                f"Updated todo: '{todo.title}'",
                f"Priority: {todo.priority.value}, Completed: {todo.completed}"
            )
        except Exception as e:
            return format_tool_response(False, f"Failed to update todo: {str(e)}")

    @tool
    async def delete_todo(text: str) -> str:
        """Delete a todo by matching its title or description."""
        try:
            success = await service.delete_by_text(text)
            
            if not success:
                return format_tool_response(False, f"Todo not found matching: '{text}'")
            
            return format_tool_response(True, f"Deleted todo matching: '{text}'")
        except Exception as e:
            return format_tool_response(False, f"Failed to delete todo: {str(e)}")

    @tool
    async def mark_complete(text: str) -> str:
        """Mark a todo as completed by matching its title or description."""
        try:
            todo = await service.update_by_text(
                text,
                TodoUpdate(completed=True)
            )
            
            if not todo:
                return format_tool_response(False, f"Todo not found matching: '{text}'")
            
            return format_tool_response(True, f"Marked as complete: '{todo.title}'")
        except Exception as e:
            return format_tool_response(False, f"Failed to mark complete: {str(e)}")

    @tool
    async def mark_incomplete(text: str) -> str:
        """Mark a todo as incomplete by matching its title or description."""
        try:
            todo = await service.update_by_text(
                text,
                TodoUpdate(completed=False)
            )
            
            if not todo:
                return format_tool_response(False, f"Todo not found matching: '{text}'")
            
            return format_tool_response(True, f"Marked as incomplete: '{todo.title}'")
        except Exception as e:
            return format_tool_response(False, f"Failed to mark incomplete: {str(e)}")

    @tool
    async def get_todos_by_priority(priority: str, page: int = 1) -> str:
        """Get todos filtered by priority level (low, medium, high, urgent) with pagination."""
        try:
            # Validate priority
            priority_enum = validate_priority(priority)
            if not priority_enum:
                return format_tool_response(False, f"Invalid priority '{priority}'. Use: low, medium, high, urgent")
            
            todos = await service.get_by_priority(priority_enum)
            
            if not todos:
                return format_tool_response(True, f"No {priority} priority todos found")
            
            return format_todo_list(todos, show_status=True, page=page)
        except Exception as e:
            return format_tool_response(False, f"Failed to get todos: {str(e)}")

    @tool
    async def search_todo(search_text: str) -> str:
        """Search for ALL todos matching the text in title or description. Returns all matching results."""
        try:
            # Use search_by_text to find ALL matches
            todos = await service.search_by_text(search_text)
            
            if not todos:
                return format_tool_response(False, f"No todos found matching '{search_text}'")
            
            # If only one result, show detailed view
            if len(todos) == 1:
                todo = todos[0]
                icon = get_priority_icon(todo.priority.value)
                status = "✓ Completed" if todo.completed else "○ Incomplete"
                
                details = [
                    f"Found 1 todo matching '{search_text}':",
                    f"{icon} [{todo.id}] {todo.title}",
                    f"Status: {status}",
                    f"Priority: {todo.priority.value}",
                ]
                
                if todo.description:
                    details.append(f"Description: {todo.description}")
                
                details.append(f"Created: {todo.created_at.strftime('%Y-%m-%d %H:%M')}")
                
                return "\n".join(details)
            
            # Multiple results - show list view
            lines = [f"Found {len(todos)} todos matching '{search_text}':"]
            for todo in todos:
                lines.append(format_todo_line(todo, show_status=True, show_priority=True))
            
            return "\n".join(lines)
        except Exception as e:
            return format_tool_response(False, f"Failed to search todo: {str(e)}")

    return [
        create_todo,
        list_todos,
        get_completed_todos,
        get_todos_by_priority,
        search_todo,
        update_todo,
        delete_todo,
        mark_complete,
        mark_incomplete,
    ]

