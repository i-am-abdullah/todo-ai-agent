from difflib import SequenceMatcher
from app.domain.models import Todo
from app.domain.schemas import TodoCreate, TodoUpdate
from app.domain.enums import TodoPriority
from app.repositories.todo_repository import TodoRepository


class TodoService:
    """Service layer for todo business logic"""

    def __init__(self, repo: TodoRepository):
        self.repo = repo

    async def create_todo(self, data: TodoCreate) -> Todo:
        """Create a new todo"""
        todo = Todo(**data.model_dump())
        return await self.repo.create(todo)

    async def list_todos(self) -> list[Todo]:
        """List all todos"""
        return await self.repo.get_all()

    async def get_by_id(self, todo_id: int) -> Todo | None:
        """Get a todo by ID"""
        return await self.repo.get_by_id(todo_id)

    async def get_by_completed(self, completed: bool) -> list[Todo]:
        """Get todos by completion status"""
        return await self.repo.get_by_completed(completed)

    async def get_by_priority(self, priority: TodoPriority) -> list[Todo]:
        """Get todos by priority level"""
        return await self.repo.get_by_priority(priority)

    async def find_by_text(self, text: str) -> Todo | None:
        """
        Find a todo by text with intelligent matching:
        1. Try exact match on title or description
        2. Try partial match
        3. Return best match using fuzzy matching
        """
        # 1. Exact match
        todo = await self.repo.get_by_exact_text(text)
        if todo:
            return todo

        # 2. Partial match
        candidates = await self.repo.get_by_partial_text(text)
        if not candidates:
            return None

        # 3. Best fuzzy match
        return max(
            candidates,
            key=lambda t: max(
                SequenceMatcher(None, text.lower(), t.title.lower()).ratio(),
                SequenceMatcher(None, text.lower(), (t.description or '').lower()).ratio(),
            ),
        )

    async def search_by_text(self, text: str, min_similarity: float = 0.6) -> list[Todo]:
        """
        Search for ALL todos matching the text (not just best match).
        Returns all todos above the similarity threshold.
        """
        # Get all potential candidates
        candidates = await self.repo.get_by_partial_text(text)
        if not candidates:
            return []

        # Calculate similarity scores and filter
        results = []
        for todo in candidates:
            title_ratio = SequenceMatcher(None, text.lower(), todo.title.lower()).ratio()
            desc_ratio = SequenceMatcher(None, text.lower(), (todo.description or '').lower()).ratio()
            max_ratio = max(title_ratio, desc_ratio)
            
            if max_ratio >= min_similarity:
                results.append((todo, max_ratio))
        
        # Sort by similarity (highest first)
        results.sort(key=lambda x: x[1], reverse=True)
        
        return [todo for todo, _ in results]

    async def update_by_id(self, todo_id: int, data: TodoUpdate) -> Todo | None:
        """Update a todo by ID"""
        todo = await self.repo.get_by_id(todo_id)
        if not todo:
            return None
        
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(todo, field, value)
        
        return await self.repo.update(todo)

    async def update_by_text(self, text: str, data: TodoUpdate) -> Todo | None:
        """Update a todo by matching title or description"""
        todo = await self.find_by_text(text)
        if not todo:
            return None
        
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(todo, field, value)
        
        return await self.repo.update(todo)

    async def delete_by_id(self, todo_id: int) -> bool:
        """Delete a todo by ID"""
        todo = await self.repo.get_by_id(todo_id)
        if not todo:
            return False
        await self.repo.delete(todo)
        return True

    async def delete_by_text(self, text: str) -> bool:
        """Delete a todo by matching title or description"""
        todo = await self.find_by_text(text)
        if not todo:
            return False
        await self.repo.delete(todo)
        return True

    async def delete_all(self) -> int:
        """Delete all todos and return count"""
        return await self.repo.delete_all()

