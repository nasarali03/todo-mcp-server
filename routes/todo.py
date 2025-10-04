from fastapi import APIRouter, HTTPException
from typing import List
from datetime import datetime
import sys
import os

# Add parent directory to path to import models
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models import Todo, TodoCreate, TodoUpdate

# Create router
router = APIRouter(prefix="/todos", tags=["todos"])

# In-memory storage for todos
todos_db: List[Todo] = []
next_id = 1


@router.post("/", response_model=Todo, status_code=201)
async def create_todo(todo: TodoCreate):
    """
    Create a new todo item.
    
    - **title**: The title of the todo item (required)
    - **description**: Optional description of the todo item
    """
    global next_id
    
    new_todo = Todo(
        id=next_id,
        title=todo.title,
        description=todo.description,
        completed=False,
        created_at=datetime.now()
    )
    
    todos_db.append(new_todo)
    next_id += 1
    
    return new_todo


@router.get("/", response_model=List[Todo])
async def get_all_todos():
    """
    Get all todo items.
    
    Returns a list of all todo items in the system.
    """
    return todos_db


@router.get("/{todo_id}", response_model=Todo)
async def get_todo(todo_id: int):
    """
    Get a single todo item by ID.
    
    - **todo_id**: The ID of the todo item to retrieve
    """
    for todo in todos_db:
        if todo.id == todo_id:
            return todo
    
    raise HTTPException(status_code=404, detail="Todo not found")


@router.put("/{todo_id}", response_model=Todo)
async def update_todo(todo_id: int, todo_update: TodoUpdate):
    """
    Update a todo item by ID.
    
    - **todo_id**: The ID of the todo item to update
    - **title**: Optional new title
    - **description**: Optional new description  
    - **completed**: Optional completion status
    """
    for i, todo in enumerate(todos_db):
        if todo.id == todo_id:
            # Update only provided fields
            update_data = todo_update.dict(exclude_unset=True)
            updated_todo = todo.copy(update=update_data)
            todos_db[i] = updated_todo
            return updated_todo
    
    raise HTTPException(status_code=404, detail="Todo not found")


@router.delete("/{todo_id}")
async def delete_todo(todo_id: int):
    """
    Delete a todo item by ID.
    
    - **todo_id**: The ID of the todo item to delete
    """
    for i, todo in enumerate(todos_db):
        if todo.id == todo_id:
            deleted_todo = todos_db.pop(i)
            return {"message": f"Todo '{deleted_todo.title}' deleted successfully"}
    
    raise HTTPException(status_code=404, detail="Todo not found")
