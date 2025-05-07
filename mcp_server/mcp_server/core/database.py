"""
Database module for FastMCP server.

This module provides database functionality for storing and retrieving metrics.
"""

import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
from neo4j import AsyncGraphDatabase
from neo4j.exceptions import ServiceUnavailable, AuthError, ClientError
from mcp_server.core.config.settings import settings


logger = logging.getLogger(__name__)

class DatabaseError(Exception):
    """Base exception for database operations."""
    pass

class ConnectionError(DatabaseError):
    """Raised when there are issues connecting to the database."""
    pass

class QueryError(DatabaseError):
    """Raised when there are issues executing queries."""
    pass

class MetricsDatabase:
    """Database class for metrics storage."""

    def __init__(self):
        self.driver = None
        self.uri = settings.NEO4J_URI
        self.user = settings.NEO4J_USER
        self.password = settings.NEO4J_PASSWORD

    async def connect(self):
        """Connect to the Neo4j database."""
        try:
            self.driver = AsyncGraphDatabase.driver(
                self.uri,
                auth=(self.user, self.password)
            )
            # Verify connection
            async with self.driver.session() as session:
                await session.run("RETURN 1")
            logger.info("Successfully connected to Neo4j")
        except Exception as e:
            logger.error(f"Failed to connect to Neo4j: {e}")
            raise

    async def disconnect(self):
        """Close the database connection."""
        if self.driver:
            await self.driver.close()
            self.driver = None
            logger.info("Disconnected from Neo4j")

    async def get_metrics(self) -> List[Dict[str, Any]]:
        """Get all metrics."""
        async with self.driver.session() as session:
            result = await session.run(
                "MATCH (m:Metric) RETURN m.name as name, m.description as description"
            )
            return [dict(record) async for record in result]

    async def search_metric_by_name(self, name: str) -> List[Dict[str, Any]]:
        """Search metrics by name."""
        async with self.driver.session() as session:
            result = await session.run(
                "MATCH (m:Metric) WHERE m.name CONTAINS $name "
                "RETURN m.name as name, m.description as description",
                name=name
            )
            return [dict(record) async for record in result]

    async def search_dashboard_by_name(self, name: str) -> List[Dict[str, Any]]:
        """Search dashboards by name."""
        async with self.driver.session() as session:
            result = await session.run(
                "MATCH (d:Dashboard) WHERE d.name CONTAINS $name "
                "RETURN d.name as name, d.description as description",
                name=name
            )
            return [dict(record) async for record in result]

    async def get_domains(self) -> List[str]:
        """Get all domains."""
        async with self.driver.session() as session:
            result = await session.run(
                "MATCH (d:Domain) RETURN d.name as name"
            )
            return [record["name"] async for record in result]

    async def get_domain_metrics(self, domain: str) -> Dict[str, Any]:
        """Get all metrics for a domain."""
        async with self.driver.session() as session:
            result = await session.run(
                """
                MATCH (d:Domain {name: $domain})-[:CONTAINS]->(m:Metric)
                RETURN d.name as domain, collect(m) as metrics
                """,
                domain=domain
            )
            record = await result.single()
            return dict(record) if record else {"domain": domain, "metrics": []}

    async def get_dashboard_paths(
        self,
        dashboard1: str,
        dashboard2: str,
        max_hops: int = 5  # Default maximum number of hops
    ) -> List[Dict[str, Any]]:
        """Find paths between two dashboards."""
        async with self.driver.session() as session:
            result = await session.run(
                """
                MATCH path = shortestPath((d1:Dashboard {name: $d1})-[*..$max_hops]-(d2:Dashboard {name: $d2}))
                RETURN path
                """,
                d1=dashboard1,
                d2=dashboard2,
                max_hops=max_hops
            )
            paths = []
            async for record in result:
                path = record["path"]
                path_data = {
                    "nodes": [node["name"] for node in path.nodes],
                    "relationships": [
                        {
                            "start": rel.start_node["name"],
                            "end": rel.end_node["name"],
                            "type": type(rel).__name__
                        }
                        for rel in path.relationships
                    ]
                }
                paths.append(path_data)
            return paths

    # Add other methods as needed, following same pattern...

