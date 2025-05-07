# Insights App

A comprehensive application for analyzing and querying metrics data using Neo4j, FastMCP, and LLM technologies.

## 🚀 Quick Start

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/insights_app.git
   cd insights_app
   ```

2. Set up environment files:
   ```bash
   # Copy and configure environment files for each service
   cp llm/.env_template llm/.env
   cp mcp_server/.env_template mcp_server/.env
   cp frontend/.env_template frontend/.env
   
   # Edit each .env file with your specific configuration
   ```

3. Start the application:
   ```bash
   ./start_app.sh
   ```

4. Access the services:
   - Frontend UI: http://localhost:8501
   - FastMCP API: http://localhost:8000
   - LLM API: http://localhost:5005
   - Neo4j Browser: http://localhost:7474

5. Stop the application:
   ```bash
   ./stop_app.sh
   ```

## 📋 Project Overview

The Insights App is composed of several microservices working together:

- **Neo4j Database**: Stores and manages the metrics data
  - Port: 7474 (HTTP), 7687 (Bolt)
  - Default credentials: neo4j/neo4j-4dm1n
  - Custom credentials: insights_user/insights_password$123

- **FastMCP Server**: Provides access to the metrics through a standardized interface
  - Port: 8000
  - Features: Metrics analysis, relationship finding, domain connections
  - [API Documentation](mcp_server/README.md#api-documentation)

- **LLM Service**: Processes natural language queries using OpenAI's API
  - Port: 5005
  - Features: Natural language processing, context-aware responses
  - [API Documentation](llm/README.md#api-documentation)

- **Frontend**: User-friendly web interface built with Streamlit
  - Port: 8501
  - Features: Interactive chat, metric visualization, query history

## 📁 Project Structure

```
insights_app/
├── neo4j/              # Neo4j database configuration and seed data
├── mcp_server/         # FastMCP service for metrics access
├── llm/               # LLM service for query processing
├── frontend/          # Streamlit web interface
├── docker-compose.yml # Docker configuration
├── start_app.sh      # Application startup script
├── stop_app.sh       # Application shutdown script
└── README.md         # This file
```


## 📝 Notes

- Neo4j Community Edition supports only one database (`neo4j`)
- Environment variables are managed through `.env` files in each service directory
- All services are containerized and can be run using Docker Compose

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
