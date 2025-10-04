# 📝 To-Do API with MCP Server

<div align="center">

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![MCP](https://img.shields.io/badge/MCP-Protocol-blue?style=for-the-badge)
![License](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)

**A modern To-Do application with REST API and MCP server integration**

[🚀 Features](#-features) • [📦 Installation](#-installation) • [🔧 Usage](#-usage) • [📚 API Documentation](#-api-documentation) • [🎥 Demo Video](#-demo-video)

</div>

---

## 🎯 Overview

This project is a comprehensive To-Do application built with **FastAPI** and integrated with **MCP (Model Context Protocol)** server capabilities. It provides both traditional REST API endpoints and modern MCP tool-based interactions for managing tasks.

### 🌟 Key Highlights

- **Dual Interface**: Both REST API and MCP server for maximum flexibility
- **Modern Architecture**: Built with FastAPI for high performance and automatic documentation
- **Type Safety**: Full Pydantic model validation
- **Developer Friendly**: Auto-generated API docs and comprehensive error handling
- **CORS Ready**: Configured for frontend integration
- **Tool-Based Interactions**: MCP server enables AI agent integration

---

## 🚀 Features

### 📋 Core Functionality

- ✅ **Create** new todo items with title and description
- 📖 **Read** all todos or individual items by ID
- ✏️ **Update** todo items (title, description, completion status)
- 🗑️ **Delete** todo items
- 📊 **Summary Statistics** with completion rates

### 🛠️ Technical Features

- **REST API Endpoints** for traditional web integration
- **MCP Server Integration** for AI agent interactions
- **Auto-generated Documentation** (Swagger UI & ReDoc)
- **CORS Support** for cross-origin requests
- **Type Validation** with Pydantic models
- **Error Handling** with proper HTTP status codes
- **Health Check** endpoint for monitoring

### 🎯 MCP Tools Available

- `create_todo` - Create new todo items
- `list_todos` - Get all todos
- `get_todo` - Get specific todo by ID
- `update_todo` - Update existing todos
- `delete_todo` - Remove todos
- `todo_summary` - Get statistics and completion rates

---

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Step 1: Clone the Repository

```bash
git clone <your-repo-url>
cd mcp
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Run the Application

```bash
# Development server with auto-reload
uvicorn main:app --reload

# Or run directly
python main.py
```

---

## 🔧 Usage

### 🌐 Access Points

Once the server is running, you can access:

| Service              | URL                          | Description              |
| -------------------- | ---------------------------- | ------------------------ |
| **API Root**         | http://localhost:8000        | Basic API information    |
| **Interactive Docs** | http://localhost:8000/docs   | Swagger UI documentation |
| **Alternative Docs** | http://localhost:8000/redoc  | ReDoc documentation      |
| **MCP Server**       | http://localhost:8000/mcp    | MCP server interface     |
| **Health Check**     | http://localhost:8000/health | Server health status     |

### 📡 REST API Examples

#### Create a Todo

```bash
curl -X POST "http://localhost:8000/todos/" \
     -H "Content-Type: application/json" \
     -d '{"title": "Learn FastAPI", "description": "Complete the FastAPI tutorial"}'
```

#### Get All Todos

```bash
curl -X GET "http://localhost:8000/todos/"
```

#### Update a Todo

```bash
curl -X PUT "http://localhost:8000/todos/1" \
     -H "Content-Type: application/json" \
     -d '{"completed": true}'
```

#### Delete a Todo

```bash
curl -X DELETE "http://localhost:8000/todos/1"
```

### 🤖 MCP Server Usage

#### List Available Tools

```bash
curl -X GET "http://localhost:8000/mcp/tools"
```

#### Use MCP Tools

```bash
# Create a todo via MCP
curl -X POST "http://localhost:8000/mcp/tools/create_todo" \
     -H "Content-Type: application/json" \
     -d '{"title": "MCP Todo", "description": "Created via MCP"}'

# Get todo summary
curl -X GET "http://localhost:8000/mcp/resources/todo_summary"
```

---

## 📚 API Documentation

### 📋 Todo Model

```python
{
    "id": int,           # Unique identifier
    "title": str,        # Todo title (required)
    "description": str,  # Optional description
    "completed": bool,   # Completion status (default: false)
    "created_at": datetime  # Creation timestamp
}
```

### 🔗 Endpoints

#### REST API Endpoints

| Method   | Endpoint      | Description       |
| -------- | ------------- | ----------------- |
| `GET`    | `/`           | API information   |
| `GET`    | `/health`     | Health check      |
| `GET`    | `/todos/`     | Get all todos     |
| `POST`   | `/todos/`     | Create new todo   |
| `GET`    | `/todos/{id}` | Get specific todo |
| `PUT`    | `/todos/{id}` | Update todo       |
| `DELETE` | `/todos/{id}` | Delete todo       |

#### MCP Server Endpoints

| Method | Endpoint                         | Description              |
| ------ | -------------------------------- | ------------------------ |
| `GET`  | `/mcp/`                          | MCP server info          |
| `GET`  | `/mcp/tools`                     | List available tools     |
| `POST` | `/mcp/tools/{tool_name}`         | Execute MCP tool         |
| `GET`  | `/mcp/resources`                 | List available resources |
| `GET`  | `/mcp/resources/{resource_name}` | Get MCP resource         |

---

## 🎥 Demo Video

<div align="center">

### 🎬 Watch the Project Demo

[![Demo Video](https://img.shields.io/badge/📹_Watch_Demo-Video-red?style=for-the-badge)](./nasarali.mp4)

**Click the button above or the video below to watch the complete project demonstration!**

<video width="800" controls>
  <source src="./nasarali.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

_This video demonstrates the complete functionality of the To-Do API with MCP Server integration_

</div>

---

## 🏗️ Project Structure

```
mcp/
├── 📁 routes/
│   ├── __pycache__/
│   └── todo.py              # Todo route handlers
├── 📄 main.py               # FastAPI application & MCP server
├── 📄 models.py             # Pydantic data models
├── 📄 requirements.txt      # Python dependencies
├── 📄 mcp_server.json       # MCP server configuration
├── 📄 nasarali.mp4          # Demo video
├── 📄 README.md             # This file
└── 📄 LICENSE               # MIT License
```

---

## 🛠️ Development

### 🔧 Configuration

The application uses the following configuration:

- **Host**: `0.0.0.0` (all interfaces)
- **Port**: `8000`
- **Auto-reload**: Enabled in development
- **CORS**: Configured for all origins (adjust for production)

### 📝 Adding New Features

1. **New API Endpoints**: Add to `routes/todo.py`
2. **New MCP Tools**: Add to `main.py` with `@mcp.tool()` decorator
3. **New Models**: Add to `models.py`
4. **Dependencies**: Update `requirements.txt`

### 🧪 Testing

```bash
# Test the API endpoints
curl -X GET "http://localhost:8000/health"

# Test MCP server
curl -X GET "http://localhost:8000/mcp/"
```

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### 📋 Contribution Guidelines

- Follow PEP 8 style guidelines
- Add tests for new features
- Update documentation as needed
- Ensure all tests pass

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Nasar Ali**

- **GitHub**: [@nasarali](https://github.com/nasarali)
- **Project**: To-Do API with MCP Server
- **Video**: [Watch Demo](./nasarali.mp4)

---

## 🙏 Acknowledgments

- **FastAPI** - The modern, fast web framework for building APIs
- **Pydantic** - Data validation using Python type annotations
- **MCP Protocol** - Model Context Protocol for AI agent integration
- **Uvicorn** - Lightning-fast ASGI server

---

## 📞 Support

If you have any questions or need help:

1. **Check** the [API Documentation](http://localhost:8000/docs)
2. **Watch** the [Demo Video](./nasarali.mp4)
3. **Open** an issue on GitHub
4. **Contact** the author

---

<div align="center">

**⭐ Star this repository if you found it helpful!**

[![GitHub stars](https://img.shields.io/github/stars/nasarali/mcp?style=social)](https://github.com/nasarali/mcp)
[![GitHub forks](https://img.shields.io/github/forks/nasarali/mcp?style=social)](https://github.com/nasarali/mcp)

_Built with ❤️ using FastAPI and MCP_

</div>
