"""Simple configuration for MCP Server."""

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import Optional


class Settings(BaseSettings):
    """MCP Server settings."""
    
    # Environment
    debug: bool = Field(default=False, alias="DEBUG")
    
    # Google Places API
    google_places_api_key: str = Field(..., alias="GOOGLE_PLACES_API_KEY")
    
    # Database
    database_url: str = Field(default="sqlite:///./food_travel.db", alias="DATABASE_URL")
    
    # Cache
    cache_dir: str = Field(default="./cache", alias="CACHE_DIR")
    cache_ttl_seconds: int = Field(default=3600, alias="CACHE_TTL")
    
    # Restaurant Search Limits
    max_search_radius_km: int = Field(default=50, alias="MAX_SEARCH_RADIUS")
    max_restaurants_per_search: int = Field(default=20, alias="MAX_RESTAURANTS")
    
    # Your existing backend (for future integration)
    backend_base_url: str = Field(default="http://localhost:5000", alias="BACKEND_BASE_URL")
    
    # Pydantic v2 settings configuration
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


# Global settings instance
settings = Settings()