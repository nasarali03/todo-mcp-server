"""
FastAPI To-Do Application with MCP Server

A simple To-Do application with CRUD operations for managing tasks.
Includes both REST API endpoints and MCP server for tool-based interactions.

To run the application:
    uvicorn main:app --reload

The application will be available at:
    - API: http://localhost:8000
    - Interactive API docs: http://localhost:8000/docs
    - Alternative API docs: http://localhost:8000/redoc
    - MCP Server: http://localhost:8000/mcp

Features:
- Create, read, update, and delete todo items
- In-memory storage (can be replaced with database later)
- Pydantic models for request/response validation
- Comprehensive error handling
- Auto-generated API documentation
- MCP server integration for tool-based interactions
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from routes.todo import router as todo_router
from typing import List, Dict, Any
import json
import asyncio
from datetime import datetime

# Create FastAPI application
app = FastAPI(
    title="To-Do API with MCP Server",
    description="A simple To-Do application with CRUD operations and MCP server integration",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include todo routes
app.include_router(todo_router)

# Import todo database and functions from routes
from routes.todo import todos_db, next_id
from models import Todo, TodoCreate, TodoUpdate

# MCP Server Implementation
class MCPServer:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.tools = {}
        self.resources = {}
    
    def tool(self, func=None):
        """Decorator to register MCP tools"""
        def decorator(f):
            self.tools[f.__name__] = {
                "function": f,
                "description": f.__doc__ or "",
                "parameters": self._get_function_params(f)
            }
            return f
        
        if func is None:
            return decorator
        else:
            return decorator(func)
    
    def resource(self, func=None):
        """Decorator to register MCP resources"""
        def decorator(f):
            self.resources[f.__name__] = {
                "function": f,
                "description": f.__doc__ or ""
            }
            return f
        
        if func is None:
            return decorator
        else:
            return decorator(func)
    
    def _get_function_params(self, func):
        """Extract function parameters for MCP tool definition"""
        import inspect
        sig = inspect.signature(func)
        params = {}
        for name, param in sig.parameters.items():
            if name == 'self':
                continue
            param_info = {
                "type": param.annotation.__name__ if param.annotation != inspect.Parameter.empty else "str",
                "required": param.default == inspect.Parameter.empty
            }
            if param.default != inspect.Parameter.empty:
                param_info["default"] = param.default
            params[name] = param_info
        return params
    
    def as_fastapi(self):
        """Convert MCP server to FastAPI app"""
        from fastapi import FastAPI as FastAPIApp
        
        mcp_app = FastAPIApp(title=f"MCP Server: {self.name}")
        
        @mcp_app.get("/")
        async def mcp_info():
            return {
                "name": self.name,
                "description": self.description,
                "tools": list(self.tools.keys()),
                "resources": list(self.resources.keys())
            }
        
        @mcp_app.post("/tools/{tool_name}")
        async def call_tool(tool_name: str, args: Dict[str, Any]):
            if tool_name not in self.tools:
                raise HTTPException(status_code=404, detail=f"Tool {tool_name} not found")
            
            try:
                result = self.tools[tool_name]["function"](**args)
                return {"result": result}
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
        @mcp_app.get("/tools")
        async def list_tools():
            return {
                "tools": {
                    name: {
                        "description": tool["description"],
                        "parameters": tool["parameters"]
                    }
                    for name, tool in self.tools.items()
                }
            }
        
        @mcp_app.get("/resources/{resource_name}")
        async def get_resource(resource_name: str):
            if resource_name not in self.resources:
                raise HTTPException(status_code=404, detail=f"Resource {resource_name} not found")
            
            try:
                result = self.resources[resource_name]["function"]()
                return {"result": result}
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
        @mcp_app.get("/resources")
        async def list_resources():
            return {
                "resources": {
                    name: {"description": resource["description"]}
                    for name, resource in self.resources.items()
                }
            }
        
        return mcp_app

# Initialize MCP Server
mcp = MCPServer(
    name="todo-mcp-server",
    description="MCP server for managing To-Do tasks"
)

# MCP Tools
@mcp.tool()
def create_todo(title: str, description: str = None) -> Dict[str, Any]:
    """
    Create a new todo item.
    
    Args:
        title: The title of the todo item
        description: Optional description of the todo item
        
    Returns:
        Dict containing the created todo item
    """
    global next_id
    
    new_todo = Todo(
        id=next_id,
        title=title,
        description=description,
        completed=False,
        created_at=datetime.now()
    )
    
    todos_db.append(new_todo)
    next_id += 1
    
    return {
        "id": new_todo.id,
        "title": new_todo.title,
        "description": new_todo.description,
        "completed": new_todo.completed,
        "created_at": new_todo.created_at.isoformat()
    }

@mcp.tool()
def list_todos() -> List[Dict[str, Any]]:
    """
    Get all todo items.
    
    Returns:
        List of all todo items
    """
    return [
        {
            "id": todo.id,
            "title": todo.title,
            "description": todo.description,
            "completed": todo.completed,
            "created_at": todo.created_at.isoformat()
        }
        for todo in todos_db
    ]

@mcp.tool()
def get_todo(id: int) -> Dict[str, Any]:
    """
    Get a single todo item by ID.
    
    Args:
        id: The ID of the todo item to retrieve
        
    Returns:
        Dict containing the todo item
    """
    for todo in todos_db:
        if todo.id == id:
            return {
                "id": todo.id,
                "title": todo.title,
                "description": todo.description,
                "completed": todo.completed,
                "created_at": todo.created_at.isoformat()
            }
    
    raise ValueError(f"Todo with ID {id} not found")

@mcp.tool()
def update_todo(id: int, title: str = None, description: str = None, completed: bool = None) -> Dict[str, Any]:
    """
    Update a todo item by ID.
    
    Args:
        id: The ID of the todo item to update
        title: Optional new title
        description: Optional new description
        completed: Optional completion status
        
    Returns:
        Dict containing the updated todo item
    """
    for i, todo in enumerate(todos_db):
        if todo.id == id:
            # Update only provided fields
            update_data = {}
            if title is not None:
                update_data["title"] = title
            if description is not None:
                update_data["description"] = description
            if completed is not None:
                update_data["completed"] = completed
            
            updated_todo = todo.copy(update=update_data)
            todos_db[i] = updated_todo
            
            return {
                "id": updated_todo.id,
                "title": updated_todo.title,
                "description": updated_todo.description,
                "completed": updated_todo.completed,
                "created_at": updated_todo.created_at.isoformat()
            }
    
    raise ValueError(f"Todo with ID {id} not found")

@mcp.tool()
def delete_todo(id: int) -> Dict[str, str]:
    """
    Delete a todo item by ID.
    
    Args:
        id: The ID of the todo item to delete
        
    Returns:
        Dict containing deletion confirmation message
    """
    for i, todo in enumerate(todos_db):
        if todo.id == id:
            deleted_todo = todos_db.pop(i)
            return {"message": f"Todo '{deleted_todo.title}' deleted successfully"}
    
    raise ValueError(f"Todo with ID {id} not found")

# MCP Resource
@mcp.resource()
def todo_summary() -> str:
    """
    Get a summary of all todos including counts.
    
    Returns:
        JSON string containing todo summary statistics
    """
    total_todos = len(todos_db)
    completed_todos = sum(1 for todo in todos_db if todo.completed)
    pending_todos = total_todos - completed_todos
    
    summary = {
        "total_todos": total_todos,
        "completed_todos": completed_todos,
        "pending_todos": pending_todos,
        "completion_rate": (completed_todos / total_todos * 100) if total_todos > 0 else 0
    }
    
    return json.dumps(summary, indent=2)

# Root endpoint
@app.get("/")
async def root():
    """
    Root endpoint providing basic information about the API.
    """
    return {
        "message": "Welcome to the To-Do API with MCP Server!",
        "docs": "/docs",
        "redoc": "/redoc",
        "todos": "/todos",
        "mcp": "/mcp",
        "features": [
            "REST API endpoints for CRUD operations",
            "MCP server for tool-based interactions",
            "Auto-generated API documentation",
            "CORS support for frontend integration"
        ]
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    """
    Health check endpoint to verify the API is running.
    """
    return {"status": "healthy", "message": "API is running"}

# Mount MCP server at /mcp endpoint
app.mount("/mcp", mcp.as_fastapi())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)