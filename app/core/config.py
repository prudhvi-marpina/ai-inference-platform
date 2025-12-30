"""
Application Configuration

This module handles all configuration using pydantic-settings.
It loads settings from environment variables and .env files.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    
    Settings are loaded in this order (first found wins):
    1. Environment variables
    2. .env file
    3. Default values (if specified)
    """
    
    # Application Settings
    service_name: str = "ai-inference-platform"
    service_version: str = "1.0.0"
    environment: str = "development"  # development, staging, production
    debug: bool = False
    
    # API Settings
    api_host: str = "0.0.0.0"  # 0.0.0.0 means listen on all interfaces
    api_port: int = 8000
    
    # Redis Configuration
    redis_url: str = "redis://127.0.0.1:6379/0"  # Use 127.0.0.1 instead of localhost for Docker on Windows
    redis_ttl: int = 60  # Cache TTL in seconds
    
    # Rate Limiting
    rate_limit_enabled: bool = True
    rate_limit_per_minute: int = 10
    rate_limit_per_hour: int = 100
    
    # OpenTelemetry (Tracing)
    otel_enabled: bool = True
    otel_exporter_otlp_endpoint: Optional[str] = None  # e.g., "http://localhost:4317"
    otel_service_name: str = "ai-inference-platform"
    
    # Model Configuration
    model_name: str = "default-model"
    model_version: str = "1.0.0"
    model_max_tokens: int = 1000
    model_temperature: float = 0.7
    
    # Logging
    log_level: str = "INFO"  # DEBUG, INFO, WARNING, ERROR
    
    # Model configuration for loading settings
    model_config = SettingsConfigDict(
        env_file=".env",           # Load from .env file
        env_file_encoding="utf-8",  # File encoding
        case_sensitive=False,       # Environment variable names are case-insensitive
        extra="ignore",             # Ignore extra environment variables
        protected_namespaces=()     # Allow fields starting with "model_"
    )


# Create a global settings instance
# This will be imported and used throughout the application
settings = Settings()

