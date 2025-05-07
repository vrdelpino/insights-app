# FastMCP Server

A powerful metrics analysis service that provides access to metrics data and supports LLM-powered insights.

## 🚀 Quick Start

1. Copy the environment template:
   ```bash
   cp .env_template .env
   ```

2. Configure your environment:
   - Set Neo4j connection details
   - Adjust other settings as needed

3. Start the service:
   ```bash
   python -m mcp_server
   ```

## 📋 Features

- Metrics Analysis
  - List and search metrics
  - Find relationships between dashboards
  - Analyze domain connections
  - Path finding between metrics and dashboards

- LLM Integration
  - Natural language query processing
  - Context-aware responses
  - Chat history support

## 🔧 Configuration

Required environment variables:
- `NEO4J_URI`: Neo4j database URI
- `NEO4J_USER`: Neo4j username
- `NEO4J_PASSWORD`: Neo4j password
- `HOST`: Server host (default: 0.0.0.0)
- `PORT`: Server port (default: 8000)
- `LOG_LEVEL`: Logging level (default: INFO)


## 📁 Project Structure

```
mcp_server/
├── mcp_server/
│   ├── __init__.py
│   ├── __main__.py          # Main application entry point
│   └── core/
│       ├── __init__.py
│       ├── agents.py        # LLM agent implementation
│       ├── database.py      # Neo4j database interface
│       └── config/
│           ├── __init__.py
│           └── settings.py  # Application settings
├── pyproject.toml          # Project configuration
└── README.md
```

## 📝 Notes
- Requires a running Neo4j instance
- Supports both REST and SSE endpoints
- Includes comprehensive test coverage
