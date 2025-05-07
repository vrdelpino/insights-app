# agent_server.py

"""
FastAPI server for the LLM Agent.

Provides HTTP endpoints for interacting with the LLM agent.
"""

from typing import Dict, List, Optional, Any
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import json

from llm.agents.executor import AgentManager
from llm.config import config

# Request/Response Models
class ChatMessage(BaseModel):
    role: str
    content: str
    timestamp: str = ""
    type: str = "text"
    metrics: Optional[List[str]] = None
    metric_details: Optional[Dict[str, Any]] = None
    domain_metrics: Optional[List[str]] = None
    dashboard_metrics: Optional[List[str]] = None

class QueryContext(BaseModel):
    chat_history: List[ChatMessage]
    current_time: str

class QueryRequest(BaseModel):
    query: str
    context: QueryContext

# Global agent manager
agent_manager = AgentManager()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await agent_manager.initialize()
    yield
    await agent_manager.cleanup()

app = FastAPI(
    title="LLM Agent API",
    lifespan=lifespan,
    host=config.server.host,
    port=config.server.port
)

@app.post("/query")
async def query_agent(request: QueryRequest):
    try:
        print(f"[DEBUG] 🔍 Received query: {request.query}")
        print(f"[DEBUG] 📜 Chat history length: {len(request.context.chat_history)}")

        formatted_history = []
        for msg in request.context.chat_history:
            formatted_history.append({
                "type": "human" if msg.role == "user" else "assistant",
                "content": msg.content
            })
            if msg.metrics:
                formatted_history.append({
                    "type": "system",
                    "content": f"Available metrics: {', '.join(msg.metrics)}"
                })
            if msg.metric_details:
                formatted_history.append({
                    "type": "system",
                    "content": f"Metric details: {json.dumps(msg.metric_details, indent=2)}"
                })
            if msg.domain_metrics:
                formatted_history.append({
                    "type": "system",
                    "content": f"Domain metrics: {', '.join(msg.domain_metrics)}"
                })
            if msg.dashboard_metrics:
                formatted_history.append({
                    "type": "system",
                    "content": f"Dashboard metrics: {', '.join(msg.dashboard_metrics)}"
                })

        result = await agent_manager.execute_query(
            query=request.query,
            chat_history=formatted_history
        )
        return JSONResponse(result)
    except Exception as e:
        print(f"[ERROR] Query failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    if not agent_manager.agent_executor:
        return {"status": "initializing"}
    return {"status": "healthy"}
