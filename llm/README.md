# LLM Service

The LLM service processes natural language queries and returns structured responses using OpenAI's API.

## 🚀 Quick Start

1. Copy the environment template:
   ```bash
   cp .env_template .env
   ```

2. Configure your environment:
   - Add your OpenAI API key
   - Adjust other settings as needed

3. Start the service:
   ```bash
   uvicorn llm.agent_server:app --host 0.0.0.0 --port 5005
   ```

## 📋 API Documentation

### Base URL
```
http://localhost:5005
```

### Endpoints

#### POST /query
Process a natural language query about metrics.

**Request Body:**
```json
{
  "query": "string",
  "context": {
    "start_time": "string",
    "end_time": "string",
    "metrics": ["string"]
  }
}
```

**Response:**
```json
{
  "query": "string",
  "response": "string",
  "metrics": [
    {
      "id": "string",
      "name": "string",
      "value": "number",
      "unit": "string"
    }
  ],
  "timestamp": "string"
}
```

#### GET /health
Check the health status of the LLM service.

**Response:**
```json
{
  "status": "string",
  "openai_status": "string",
  "fastmcp_status": "string",
  "timestamp": "string"
}
```

## 🔧 Configuration

Required environment variables:
- `OPENAI_API_KEY`: Your OpenAI API key
- `FASTMCP_URL`: URL of the FastMCP service (default: http://mcp_server:8000)
- `HOST`: Server host (default: 0.0.0.0)
- `PORT`: Server port (default: 5005)
- `LOG_LEVEL`: Logging level (default: INFO)

## 📝 Notes
- The service requires a valid OpenAI API key
- Health checks are performed periodically
- All API endpoints are documented with OpenAPI/Swagger
