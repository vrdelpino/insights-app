#!/bin/bash

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to open URL in default browser
open_url() {
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        open "$1"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        xdg-open "$1"
    elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
        # Windows
        start "$1"
    else
        echo "Could not detect OS to open browser automatically"
        echo "Please open the URL manually: $1"
    fi
}

# Determine which compose command to use
if command_exists docker-compose; then
    COMPOSE_CMD="docker-compose"
elif command_exists docker && docker compose version >/dev/null 2>&1; then
    COMPOSE_CMD="docker compose"
else
    echo "Error: Neither docker-compose nor docker compose is available"
    exit 1
fi

# Start the entire application stack
echo "Starting Insights App..."
$COMPOSE_CMD up -d

# Wait for services to be ready
echo "Waiting for services to be ready..."
sleep 5

# Check if services are running
echo "Checking service status..."
$COMPOSE_CMD ps

echo "Insights App is running!"
echo "Streamlit UI: http://localhost:8501"
echo "FastMCP API: http://localhost:8000"
echo "LLM API: http://localhost:5005"

# Open Streamlit in default browser
echo "Opening Streamlit UI in your default browser..."
open_url "http://localhost:8501" 