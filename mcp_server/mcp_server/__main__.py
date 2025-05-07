"""
FastMCP Insights Analysis Tool main entry point.
"""

import asyncio
import logging
import signal
import sys
from typing import List, Dict, Any
from pydantic import Field, BaseModel
from fastmcp import FastMCP, Context
from mcp_server.core.database import MetricsDatabase
from mcp_server.core.config.settings import settings
from mcp_server.core.agents import AgentManager
import click

# Configure logging
logging.basicConfig(level=settings.LOG_LEVEL)
logger = logging.getLogger(__name__)

# Initialize services
db = MetricsDatabase()
agent_manager = AgentManager()

# Pydantic models for chat
class ChatMessage(BaseModel):
    role: str
    content: str

class ChatContext(BaseModel):
    chat_history: List[ChatMessage]

class QueryRequest(BaseModel):
    query: str
    context: ChatContext

async def wait_for_database():
    max_retries = 5
    retry_delay = 5  # seconds
    for attempt in range(max_retries):
        try:
            await db.connect()
            logger.info("Successfully connected to database!")
            return
        except Exception as e:
            if attempt < max_retries - 1:
                logger.warning(f"Failed to connect to database (attempt {attempt + 1}/{max_retries}): {e}")
                logger.info(f"Retrying in {retry_delay} seconds...")
                await asyncio.sleep(retry_delay)
            else:
                logger.error(f"Failed to connect to database after {max_retries} attempts: {e}")
                raise

async def run_server():
    await wait_for_database()
    await agent_manager.initialize()

    mcp = FastMCP("insights-analysis-tool", port=settings.PORT, log_level=settings.LOG_LEVEL, debug=True)

    # Metrics Tools
    @mcp.tool()
    async def list_metrics(ctx: Context = None) -> List[str]:
        """List all available metric names."""
        if ctx:
            await ctx.info("Fetching all metrics...")
        try:
            metrics = await db.get_metrics()
            logger.info(f"Retrieved {len(metrics)} metrics from database")
            if not metrics:
                logger.warning("No metrics found in database")
            return [metric["name"] for metric in metrics]
        except Exception as e:
            logger.error(f"Error fetching metrics: {str(e)}")
            if ctx:
                await ctx.error(f"Error fetching metrics: {str(e)}")
            raise

    @mcp.tool()
    async def search_metrics(name: str = Field(default="", description="Name of the metric to search for"), ctx: Context = None) -> List[Dict[str, Any]]:
        """Search for metrics by name."""
        if ctx:
            await ctx.info(f"Searching for metrics matching '{name}'...")
        return await db.search_metric_by_name(name)

    @mcp.tool()
    async def list_dashboards(name: str = Field(default="", description="Name of the dashboard to search for"), ctx: Context = None) -> List[Dict[str, Any]]:
        """Search dashboards by name."""
        if ctx:
            await ctx.info(f"Searching for dashboards matching '{name}'...")
        return await db.search_dashboard_by_name(name)

    @mcp.tool()
    async def list_domains(ctx: Context = None) -> List[str]:
        """List all available domains."""
        if ctx:
            await ctx.info("Fetching available domains...")
        return await db.get_domains()

    @mcp.tool()
    async def find_dashboard_path(
        dashboard1: str = Field(description="First dashboard name"),
        dashboard2: str = Field(description="Second dashboard name"),
        ctx: Context = None
    ) -> List[Dict[str, Any]]:
        """Find path between two dashboards."""
        if not dashboard1 or not dashboard2:
            if ctx:
                await ctx.error("Both dashboard names are required")
            return []
        if ctx:
            await ctx.info(f"Finding path between '{dashboard1}' and '{dashboard2}'...")
        return await db.get_dashboard_paths(dashboard1, dashboard2)

    @mcp.tool()
    async def find_domain_path(
        domain1: str = Field(description="First domain name"),
        domain2: str = Field(description="Second domain name"),
        ctx: Context = None
    ) -> List[Dict[str, Any]]:
        """Find dashboard path between two domains."""
        if not domain1 or not domain2:
            if ctx:
                await ctx.error("Both domain names are required")
            return []

        if ctx:
            await ctx.info(f"Finding paths between domains '{domain1}' and '{domain2}'...")

        domain1_dashboards = await db.get_domain_metrics(domain1)
        domain2_dashboards = await db.get_domain_metrics(domain2)

        paths = []
        for db1 in domain1_dashboards.get("metrics", []):
            for db2 in domain2_dashboards.get("metrics", []):
                dashboard_paths = await db.get_dashboard_paths(db1["name"], db2["name"])
                if dashboard_paths:
                    paths.extend(dashboard_paths)
        return paths

    # LLM Agent Tools
    @mcp.tool()
    async def process_query(
        query: str = Field(description="The query to process"),
        chat_history: List[Dict[str, str]] = Field(default=[], description="Chat history"),
        ctx: Context = None
    ) -> Dict[str, Any]:
        """Process a query through the LLM agent."""
        if ctx:
            await ctx.info(f"Processing query: {query}")
        try:
            result = await agent_manager.execute_query(
                query=query,
                chat_history=chat_history
            )
            return result
        except Exception as e:
            if ctx:
                await ctx.error(f"Error processing query: {str(e)}")
            raise

    # Resources
    @mcp.resource("config://version")
    def get_version() -> str:
        return "1.0.0"

    @mcp.resource("metrics://{metric_name}")
    async def get_metric(metric_name: str) -> Dict[str, Any]:
        metrics = await db.search_metric_by_name(metric_name)
        return metrics[0] if metrics else {}

    def signal_handler(signum, frame):
        logger.info("\nReceived termination signal. Shutting down...")
        asyncio.run(cleanup())
        sys.exit(0)

    async def cleanup():
        await agent_manager.cleanup()
        await db.disconnect()

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    await mcp.run_async(transport='sse')

@click.command()
@click.option("--port", default=settings.PORT, help="Port to listen", type=int)
def main(port: int):
    asyncio.run(run_server())

if __name__ == "__main__":
    sys.exit(main())
