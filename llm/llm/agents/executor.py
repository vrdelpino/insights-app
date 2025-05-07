# executor.py

"""
Agent execution management.

Handles initialization and execution of the LLM agent with its tools.
"""

import asyncio
import logging
from typing import Any, Dict, List, Optional

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.agents import OpenAIFunctionsAgent
from langchain.agents.format_scratchpad import format_to_openai_function_messages
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from langchain.agents import create_openai_functions_agent

from agents.mcp import MCPServerSse
from llm.config import config
from llm.agents.tools import make_structured_tool

logger = logging.getLogger(__name__)


class AgentManager:
    """Manages the lifecycle and execution of the LLM agent."""

    def __init__(self):
        self.agent_executor: Optional[AgentExecutor] = None
        self.mcp_server: Optional[MCPServerSse] = None

    async def initialize(self):
        """Initialize the agent by connecting to MCP server and setting up tools."""
        logger.info("🔄 Initializing agent...")

        max_retries = 5
        retry_delay = 5

        for attempt in range(max_retries):
            try:
                self.mcp_server = MCPServerSse(
                    params={"url": config.fastmcp_url},
                    cache_tools_list=True
                )
                await self.mcp_server.connect()
                break
            except Exception as e:
                if attempt < max_retries - 1:
                    logger.warning(f"⚠️ MCP connection failed (attempt {attempt + 1}/{max_retries}): {e}")
                    await asyncio.sleep(retry_delay)
                else:
                    logger.error(f"❌ Could not connect to MCP after {max_retries} attempts: {e}")
                    raise

        tools = [make_structured_tool(t, self.mcp_server) for t in await self.mcp_server.list_tools()]
        logger.info(f"🧰 Tools discovered: {[t.name for t in tools]}")

        llm = ChatOpenAI(
            api_key=config.openai_api_key,
            model="gpt-4",
            temperature=0
        )

        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful AI assistant that uses tools to answer questions."),
            MessagesPlaceholder(variable_name="chat_history", optional=True),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ])

        # Create the agent with the correct configuration
        from langchain.agents import create_openai_functions_agent
        from langchain.agents.format_scratchpad import format_to_openai_function_messages
        from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser

        agent = create_openai_functions_agent(
            llm=llm,
            tools=tools,
            prompt=prompt
        )

        # Create the executor with the agent
        self.agent_executor = AgentExecutor.from_agent_and_tools(
            agent=agent,
            tools=tools,
            verbose=True,
            return_intermediate_steps=True,
            handle_parsing_errors=True,
            max_iterations=3
        )

        logger.info("✅ Agent initialized successfully")

    async def cleanup(self):
        """Clean up resources when shutting down."""
        if self.mcp_server:
            await self.mcp_server.disconnect()
            self.mcp_server = None
        self.agent_executor = None

    async def execute_query(self, query: str, chat_history: Optional[List] = None) -> Dict[str, Any]:
        """Execute a query using the agent and return results with step-by-step info."""
        if not self.agent_executor:
            raise RuntimeError("Agent not initialized")

        chat_history = chat_history or []

        result = await self.agent_executor.ainvoke({
            "input": query,
            "chat_history": chat_history
        })

        tool_usage = []
        for step in result["intermediate_steps"]:
            action, observation = step
            tool_usage.append({
                "tool_name": action.tool,
                "thought": action.log,
                "tool_input": action.tool_input,
                "tool_output": observation
            })

        return {
            "final_response": result["output"],
            "tool_usage": tool_usage
        }
