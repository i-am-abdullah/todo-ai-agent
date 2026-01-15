# Todo AI Agent 🤖✅

A production-grade Todo management system powered by AI, built with FastAPI, LangChain, and Neon Postgres.

## Features

- 🤖 **Natural Language Interface**: Talk to your todos using plain English
- 🔄 **RESTful API**: Complete CRUD operations for traditional integrations
- 🗄️ **Async Database**: High-performance async SQLAlchemy with Neon Postgres
- 🧠 **Smart Matching**: Fuzzy search and intelligent todo matching
- 🏗️ **Clean Architecture**: Repository → Service → Tool → Agent pattern
- 📝 **OpenAPI Docs**: Auto-generated API documentation
- 🚀 **Production Ready**: Structured logging, error handling, and best practices

## Architecture

```
┌─────────────┐
│   FastAPI   │ ← HTTP Endpoints
└──────┬──────┘
       │
┌──────▼──────┐
│ AI Agent    │ ← LangChain Agent
│  (LLM)      │
└──────┬──────┘
       │
┌──────▼──────┐
│   Tools     │ ← LangChain Tools
└──────┬──────┘
       │
┌──────▼──────┐
│  Services   │ ← Business Logic
└──────┬──────┘
       │
┌──────▼──────┐
│ Repository  │ ← Data Access
└──────┬──────┘
       │
┌──────▼──────┐
│  Database   │ ← Neon Postgres
└─────────────┘
```

## Quick Start

### 1. Prerequisites

- Python 3.11+
- Neon Postgres account (or any Postgres database)
- OpenRouter API key (or OpenAI API key)

### 2. Installation

```bash
# Clone the repository
cd todo-ai-agent

# Install dependencies using Poetry
poetry install

# Or using pip
pip install -r requirements.txt

# Copy environment template
cp env.example .env
```

### 3. Configuration

Edit `.env` with your credentials (all three required):

```bash
DATABASE_URL=postgresql+asyncpg://user:password@your-host.neon.tech/neondb
OPENROUTER_API_KEY=sk-or-v1-your-key-here
OPENROUTER_MODEL=openai/gpt-4o-mini
```

**Note:** Use `postgresql+asyncpg://` prefix (not `postgresql://`). See `env.example` for model options.

### 4. Run the Application

```bash
# Using Poetry
poetry run uvicorn app.main:app --reload

# Or directly
uvicorn app.main:app --reload
```

The application will be available at:
- **API**: http://localhost:8000
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Usage

### REST API Examples

#### Create a Todo

```bash
curl -X POST "http://localhost:8000/api/v1/todos" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Buy groceries",
    "description": "Milk, eggs, bread"
  }'
```

#### List All Todos

```bash
curl "http://localhost:8000/api/v1/todos"
```

#### Update a Todo

```bash
curl -X PUT "http://localhost:8000/api/v1/todos/1" \
  -H "Content-Type: application/json" \
  -d '{
    "completed": true
  }'
```

### AI Agent Examples

#### Natural Language Queries

```bash
# Create a todo
curl -X POST "http://localhost:8000/api/v1/agent/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "Add a todo to call mom tomorrow"}'

# List todos
curl -X POST "http://localhost:8000/api/v1/agent/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "Show me all my incomplete tasks"}'

# Mark complete
curl -X POST "http://localhost:8000/api/v1/agent/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "Mark the groceries todo as done"}'

# Delete todo
curl -X POST "http://localhost:8000/api/v1/agent/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "Delete the todo about calling mom"}'
```

## Project Structure

```
todo-ai-agent/
├── app/
│   ├── main.py              # FastAPI app entry point
│   ├── api/                 # API layer
│   │   ├── deps.py          # Dependency injection
│   │   └── v1/
│   │       ├── router.py    # Route aggregator
│   │       ├── todos.py     # Todo endpoints
│   │       └── agent.py     # AI agent endpoints
│   ├── agents/              # LangChain agents
│   │   ├── todo_agent.py    # Agent configuration
│   │   ├── prompts.py       # System prompts
│   │   └── executor.py      # Agent executor
│   ├── tools/               # LangChain tools
│   │   ├── base.py          # Base tool utilities
│   │   ├── todo_tools.py    # Todo CRUD tools
│   │   └── tool_config.py   # Tool metadata
│   ├── services/            # Business logic
│   │   ├── todo_service.py  # Todo operations
│   │   └── agent_service.py # Agent orchestration
│   ├── repositories/        # Data access
│   │   └── todo_repository.py
│   ├── domain/              # Domain models
│   │   ├── models.py        # SQLAlchemy models
│   │   ├── schemas.py       # Pydantic schemas
│   │   └── enums.py         # Enumerations
│   ├── db/                  # Database setup
│   │   ├── base.py          # SQLAlchemy base
│   │   └── session.py       # DB sessions
│   ├── core/                # Core configuration
│   │   ├── config.py        # Settings
│   │   ├── logging.py       # Logging setup
│   │   └── security.py      # Auth (future)
│   └── utils/               # Utilities
│       ├── datetime.py
│       ├── exceptions.py
│       └── constants.py
├── scripts/
│   └── init_db.py           # Database initialization
├── .env.example             # Environment template
├── pyproject.toml           # Python dependencies
└── README.md                # This file
```

## API Endpoints

### Todos

- `POST /api/v1/todos` - Create a new todo
- `GET /api/v1/todos` - List all todos (supports `?completed=true/false`)
- `GET /api/v1/todos/{id}` - Get a specific todo
- `PUT /api/v1/todos/{id}` - Update a todo
- `DELETE /api/v1/todos/{id}` - Delete a todo

### AI Agent

- `POST /api/v1/agent/query` - Send a natural language query

### System

- `GET /` - Root endpoint
- `GET /health` - Health check

## Development

### Running Tests

```bash
poetry run pytest
```

### Code Formatting

```bash
# Format with black
poetry run black app/

# Lint with ruff
poetry run ruff check app/
```

### Database Migrations

```bash
# Create a migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `APP_NAME` | Application name | Todo AI Agent |
| `DATABASE_URL` | Postgres connection string | Required |
| `OPENROUTER_API_KEY` | OpenRouter API key | Required |
| `OPENROUTER_MODEL` | Model to use | openai/gpt-4o-mini |

## Technology Stack

- **Framework**: FastAPI
- **Database**: Neon Postgres (async SQLAlchemy)
- **AI/LLM**: LangChain + OpenRouter
- **Python**: 3.11+
- **Package Manager**: Poetry

## Future Enhancements

- [ ] User authentication & authorization
- [ ] Streaming agent responses
- [ ] Redis caching for agent sessions
- [ ] Todo priorities and tags
- [ ] Due dates and reminders
- [ ] Observability (OpenTelemetry)
- [ ] Rate limiting
- [ ] Batch operations

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - feel free to use this project for learning or production.

## Support

For issues and questions, please open an issue on GitHub.

---

Built with ❤️ using FastAPI, LangChain, and Neon Postgres

