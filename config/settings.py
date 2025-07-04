"""Simple configuration for MCP Server."""

from pydantic import BaseSettings, Field
from typing import Optional


class Settings(BaseSettings):
    """MCP Server settings."""
    
    # Environment
    debug: bool = Field(default=False, env="DEBUG")
    
    # Google Places API
    google_places_api_key: str = Field(..., env="GOOGLE_PLACES_API_KEY")
    
    # Database
    database_url: str = Field(default="sqlite:///./food_travel.db", env="DATABASE_URL")
    
    # Cache
    cache_dir: str = Field(default="./cache", env="CACHE_DIR")
    cache_ttl_seconds: int = Field(default=3600, env="CACHE_TTL")
    
    # Restaurant Search Limits
    max_search_radius_km: int = Field(default=50, env="MAX_SEARCH_RADIUS")
    max_restaurants_per_search: int = Field(default=20, env="MAX_RESTAURANTS")
    
    # Your existing backend (for future integration)
    backend_base_url: str = Field(default="http://localhost:5000", env="BACKEND_BASE_URL")
    
    class Config:
        env_file = ".env"


# Global settings instance
settings = Settings()