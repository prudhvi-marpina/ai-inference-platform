"""
Pytest Configuration and Fixtures

This file contains shared fixtures used across all tests.
Fixtures are reusable test components (like test database, mock services, etc.)
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, MagicMock, patch
import asyncio
import os

# Set test environment variable BEFORE any imports
os.environ["ENVIRONMENT"] = "test"

# Mock Redis connection BEFORE importing app
# This prevents startup_event from trying to connect to real Redis
from app.services.cache import cache_service

# Create a mock Redis client that will be used during app startup
mock_redis_client = MagicMock()
mock_redis_client.ping = AsyncMock(return_value=True)
mock_redis_client.get = AsyncMock(return_value=None)
mock_redis_client.setex = AsyncMock(return_value=True)
mock_redis_client.close = AsyncMock(return_value=None)

# Mock the connect method to use our mock client
# This MUST be done before importing app
async def mock_connect():
    """Mock connect that doesn't actually connect to Redis."""
    # Set mock client and connected state
    cache_service.redis_client = mock_redis_client
    cache_service._connected = True
    # Return immediately (no actual connection)
    return

# Replace the connect method with our mock BEFORE importing app
cache_service.connect = mock_connect
# Pre-set connected state and mock client so connect() can be a no-op
cache_service._connected = True
cache_service.redis_client = mock_redis_client

# Now import app - it will use the mocked Redis connection
from app.main import app
from app.services.model import model_service


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """
    Automatically set up test environment for all tests.
    This runs once per test session.
    """
    # Ensure Redis is mocked
    cache_service._connected = True
    cache_service.redis_client = mock_redis_client
    yield
    # Cleanup (if needed)
    pass


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
    
    Note: Redis connection is mocked automatically before app import.
    TestClient will trigger startup events, but they'll use the mocked Redis.
    """
    # Ensure mock is in place before creating TestClient
    cache_service._connected = True
    cache_service.redis_client = mock_redis_client
    
    # Create TestClient - startup events will use mocked Redis
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

