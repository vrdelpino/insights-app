# config.py

"""
Configuration module for the LLM application.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class ServerConfig(BaseSettings):
    host: str = Field(default="0.0.0.0", env="HOST")
    port: int = Field(default=5005, env="PORT")
    log_level: str = Field(default="INFO", env="LOG_LEVEL")

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        env_prefix=""
    )

    server: ServerConfig = ServerConfig()
    fastmcp_url: str = Field(default="http://mcp_server:8000/sse", env="MCP_SERVER_URL")
    openai_api_key: str = Field(env="OPENAI_API_KEY")

config = Settings()
