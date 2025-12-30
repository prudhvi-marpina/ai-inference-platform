"""
Pytest Configuration and Fixtures

This file contains shared fixtures used across all tests.
Fixtures are reusable test components (like test database, mock services, etc.)
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, MagicMock, patch
import asyncio

from app.main import app
from app.services.cache import cache_service
from app.services.model import model_service


@pytest.fixture
def client():
    """
    Create a test client for the FastAPI app.
    
    TestClient is a synchronous wrapper around FastAPI that allows us to
    make HTTP requests to our app without running a server.
    
    Why use it:
    - Fast: No network overhead
    - Easy: Simple request/response testing
    - Isolated: Each test gets a fresh client
    """
    return TestClient(app)


@pytest.fixture
def mock_redis():
    """
    Mock Redis connection for testing.
    
    This allows us to test caching without needing a real Redis server.
    We mock the Redis client methods (get, set, ping) to return expected values.
    
    Why mock:
    - No external dependencies needed
    - Tests run faster
    - Tests are more reliable (no network issues)
    
    Note: Returns AsyncMock objects for async methods, but fixture itself is sync
    so it can be used in sync tests.
    """
    from unittest.mock import AsyncMock
    
    # Store cache data in memory for testing
    cache_data = {}
    
    async def mock_get(key):
        return cache_data.get(key)
    
    async def mock_setex(key, ttl, value):
        cache_data[key] = value
        return True
    
    async def mock_ping():
        return True
    
    async def mock_close():
        return None
    
    # Create mock client with async methods
    mock_client = MagicMock()
    mock_client.ping = AsyncMock(side_effect=mock_ping)
    mock_client.get = AsyncMock(side_effect=mock_get)
    mock_client.setex = AsyncMock(side_effect=mock_setex)
    mock_client.close = AsyncMock(side_effect=mock_close)
    
    return mock_client


@pytest.fixture
def mock_redis_connected(mock_redis):
    """
    Fixture that mocks Redis and connects it to cache_service.
    
    This sets up the cache service with a mock Redis client so we can
    test caching behavior without a real Redis instance.
    
    Why synchronous:
    - TestClient from FastAPI is synchronous
    - We mock the async methods but use sync test client
    - This is simpler and works well for integration tests
    """
    # Save original client
    original_client = cache_service.redis_client
    original_connected = cache_service._connected
    
    # Replace with mock
    cache_service.redis_client = mock_redis
    cache_service._connected = True
    
    yield mock_redis
    
    # Restore original
    cache_service.redis_client = original_client
    cache_service._connected = original_connected


@pytest.fixture
def sample_inference_request():
    """
    Sample inference request data for testing.
    
    This is a reusable test data fixture that provides consistent
    test input across multiple tests.
    """
    return {
        "prompt": "What is artificial intelligence?",
        "max_tokens": 50,
        "temperature": 0.7
    }


@pytest.fixture
def sample_inference_response():
    """
    Sample inference response data for testing.
    
    This represents what the model service returns.
    """
    return {
        "output": "Model response to: What is artificial intelligence?...",
        "tokens_used": 15,
        "model_version": "1.0.0",
        "model_name": "default-model"
    }

