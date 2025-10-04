from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class TodoBase(BaseModel):
    """Base model for Todo items with common fields"""
    title: str
    description: Optional[str] = None


class TodoCreate(TodoBase):
    """Model for creating a new Todo item"""
    pass


class TodoUpdate(BaseModel):
    """Model for updating a Todo item - all fields optional"""
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


class Todo(TodoBase):
    """Model for Todo item response"""
    id: int
    completed: bool = False
    created_at: datetime

    class Config:
        from_attributes = True
