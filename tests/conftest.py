"""Pytest configuration for tests."""

import pytest
import asyncio
import os
from dotenv import load_dotenv

# Load environment variables for all tests
load_dotenv()


def pytest_configure(config):
    """Configure pytest."""
    # Add custom markers
    config.addinivalue_line(
        "markers", 
        "integration: marks tests as integration tests (may be slow)"
    )


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def check_api_key():
    """Check if Google Places API key is configured."""
    api_key = os.getenv("GOOGLE_PLACES_API_KEY")
    if not api_key or api_key == "your_google_places_api_key_here":
        pytest.skip("GOOGLE_PLACES_API_KEY not configured in .env file")
    return api_key