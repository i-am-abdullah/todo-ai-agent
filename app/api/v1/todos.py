"""
REST API endpoints for todo CRUD operations
"""

from fastapi import APIRouter, Depends, HTTPException, status
from app.api.deps import get_todo_service
from app.services.todo_service import TodoService
from app.domain.schemas import TodoCreate, TodoUpdate, TodoRead

router = APIRouter(prefix="/todos", tags=["Todos"])


@router.post("/", response_model=TodoRead, status_code=status.HTTP_201_CREATED)
async def create_todo(
    data: TodoCreate,
    service: TodoService = Depends(get_todo_service)
):
    """Create a new todo item"""
    todo = await service.create_todo(data)
    return todo


@router.get("/", response_model=list[TodoRead])
async def list_todos(
    completed: bool | None = None,
    service: TodoService = Depends(get_todo_service)
):
    """
    List todos, optionally filtered by completion status
    
    - **completed**: Filter by completion status (true/false), or omit for all
    """
    if completed is not None:
        todos = await service.get_by_completed(completed)
    else:
        todos = await service.list_todos()
    return todos


@router.get("/{todo_id}", response_model=TodoRead)
async def get_todo(
    todo_id: int,
    service: TodoService = Depends(get_todo_service)
):
    """Get a specific todo by ID"""
    todo = await service.get_by_id(todo_id)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with id {todo_id} not found"
        )
    return todo


@router.put("/{todo_id}", response_model=TodoRead)
async def update_todo(
    todo_id: int,
    data: TodoUpdate,
    service: TodoService = Depends(get_todo_service)
):
    """Update a todo by ID"""
    todo = await service.update_by_id(todo_id, data)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with id {todo_id} not found"
        )
    return todo


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
    todo_id: int,
    service: TodoService = Depends(get_todo_service)
):
    """Delete a todo by ID"""
    success = await service.delete_by_id(todo_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with id {todo_id} not found"
        )
    return None

