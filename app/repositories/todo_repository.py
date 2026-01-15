from sqlalchemy import select, or_, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import func
from app.domain.models import Todo
from app.domain.enums import TodoPriority


class TodoRepository:
    """Repository for Todo database operations"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, todo: Todo) -> Todo:
        """Create a new todo in the database"""
        self.session.add(todo)
        await self.session.commit()
        await self.session.refresh(todo)
        return todo

    async def get_all(self) -> list[Todo]:
        """Get all todos"""
        result = await self.session.execute(select(Todo))
        return list(result.scalars().all())

    async def get_by_id(self, todo_id: int) -> Todo | None:
        """Get a todo by ID"""
        result = await self.session.execute(
            select(Todo).where(Todo.id == todo_id)
        )
        return result.scalar_one_or_none()

    async def get_by_exact_text(self, text: str) -> Todo | None:
        """Get a todo by exact match on title or description"""
        result = await self.session.execute(
            select(Todo).where(
                or_(
                    func.lower(Todo.title) == text.lower(),
                    func.lower(Todo.description) == text.lower(),
                )
            )
        )
        return result.scalar_one_or_none()

    async def get_by_partial_text(self, text: str) -> list[Todo]:
        """Get todos by partial match on title or description"""
        like = f"%{text.lower()}%"
        result = await self.session.execute(
            select(Todo).where(
                or_(
                    func.lower(Todo.title).like(like),
                    func.lower(Todo.description).like(like),
                )
            )
        )
        return list(result.scalars().all())

    async def get_by_completed(self, completed: bool) -> list[Todo]:
        """Get todos filtered by completion status"""
        result = await self.session.execute(
            select(Todo).where(Todo.completed == completed)
        )
        return list(result.scalars().all())

    async def get_by_priority(self, priority: TodoPriority) -> list[Todo]:
        """Get todos filtered by priority level"""
        result = await self.session.execute(
            select(Todo).where(Todo.priority == priority.value)
        )
        return list(result.scalars().all())

    async def update(self, todo: Todo) -> Todo:
        """Update an existing todo"""
        await self.session.commit()
        await self.session.refresh(todo)
        return todo

    async def delete(self, todo: Todo) -> None:
        """Delete a todo"""
        await self.session.delete(todo)
        await self.session.commit()

    async def delete_all(self) -> int:
        """Delete all todos and return count of deleted items"""
        result = await self.session.execute(delete(Todo))
        await self.session.commit()
        return result.rowcount

