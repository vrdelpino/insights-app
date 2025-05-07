import logging
from typing import List, Optional
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from llm.agents.executor import AgentManager
from llm.config import config

# Configure logging
logging.basicConfig(level=config.server.log_level)
logger = logging.getLogger(__name__)

# Pydantic models
class ChatMessage(BaseModel):
    role: str
    content: str

class ChatContext(BaseModel):
    chat_history: List[ChatMessage]

class QueryRequest(BaseModel):
    query: str
    context: ChatContext

# Initialize FastAPI app
app = FastAPI(title="LLM Agent API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Agent manager
agent_manager = AgentManager()

@app.on_event("startup")
async def startup_event():
    """Initialize agent on app startup."""
    try:
        await agent_manager.initialize()
        logger.info("✅ Agent initialized successfully.")
    except Exception as e:
        logger.error(f"❌ Failed to initialize agent: {e}")
        raise

@app.on_event("shutdown")
async def shutdown_event():
    """Clean up agent resources on shutdown."""
    await agent_manager.cleanup()
    logger.info("🧹 Agent cleanup completed.")

@app.post("/query")
async def process_query(request: QueryRequest):
    """Endpoint to process a user query through the agent."""
    try:
        chat_history = [
            {"type": msg.role, "content": msg.content}
            for msg in request.context.chat_history
        ]
        result = await agent_manager.execute_query(
            query=request.query,
            chat_history=chat_history
        )
        return result
    except Exception as e:
        logger.error(f"⚠️ Error processing query: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("llm_app.__main__:app", host=config.server.host, port=config.server.port, reload=False)
