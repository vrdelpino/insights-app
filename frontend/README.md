# Insights App - Streamlit Frontend

A user-friendly interface for interacting with the Insights application's metrics and LLM services.

## 🚀 Quick Start

1. Copy the environment template:
   ```bash
   cp .env_template .env
   ```

2. Configure your environment:
   - Set the LLM and FastMCP service URLs
   - Adjust other settings as needed

3. Start the application:
   ```bash
   streamlit run src/main.py
   ```

## 📋 Features

- Interactive chat interface for querying metrics
- Step-by-step analysis of how answers are generated
- Available metrics listing
- Chat history persistence during session
- Clear chat functionality
- Real-time metric visualization
- Query history tracking

## 🔧 Configuration

The following environment variables are required:

- `LLM_URL`: URL of the LLM service (default: http://llm_app:5005)
- `FASTMCP_URL`: URL of the FastMCP service (default: http://fastmcp_app:8000)
- `HOST`: Server host (default: 0.0.0.0)
- `PORT`: Server port (default: 8501)
- `LOG_LEVEL`: Logging level (default: INFO)
- `SESSION_TIMEOUT`: Session timeout in minutes (default: 30)
- `MAX_HISTORY`: Maximum chat history entries (default: 50)

## 🛠️ Development

### Prerequisites
- Python 3.12
- UV package manager
- Docker and Docker Compose

### Local Setup
1. Create virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   uv pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   streamlit run src/main.py
   ```

### Docker Development
The application is designed to run in a Docker container as part of the larger Insights application stack:

```bash
docker-compose up streamlit_app
```

## 📊 API Integration

The Streamlit app communicates with two backend services:

### LLM Service (port 5005)
- Processes natural language queries
- Returns structured responses with metrics
- Provides health status information

### FastMCP Service (port 8000)
- Provides access to metrics data
- Supports metric queries with filters
- Returns metric metadata and values

## 📁 Project Structure

```
streamlit_app/
├── src/
│   ├── __init__.py
│   ├── main.py          # Main Streamlit application
│   ├── chat.py          # Chat-related functionality
│   └── metrics.py       # Metrics-related functionality
├── requirements.txt     # Python dependencies
├── Dockerfile          # Container configuration
├── .env_template       # Environment template
└── README.md           # This file
```

## 📦 Dependencies

- streamlit==1.32.0
- requests==2.32.3
- certifi==2025.4.26
- charset-normalizer==3.4.1
- idna==3.10
- urllib3==2.4.0

## 📝 Notes
- The application requires both LLM and FastMCP services to be running
- Chat history is persisted during the session
- All API endpoints are documented with OpenAPI/Swagger
- The application supports real-time updates and visualizations

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

[Your License Here]
