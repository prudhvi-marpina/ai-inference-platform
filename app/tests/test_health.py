"""
Tests for Health Check Endpoint

Tests verify that the health endpoint returns the correct status.
This is critical for Kubernetes liveness/readiness probes.
"""

import pytest
from fastapi import status


def test_health_endpoint(client):
    """
    Test that the health endpoint returns healthy status.
    
    What we're testing:
    - Endpoint exists and is accessible
    - Returns 200 status code
    - Returns correct JSON structure
    - Contains "status": "healthy"
    
    Why this matters:
    - Kubernetes uses this to check if the service is alive
    - Load balancers use this for health checks
    - Monitoring systems check this endpoint
    """
    # Make GET request to /health
    response = client.get("/health")
    
    # Assert status code is 200 (OK)
    assert response.status_code == status.HTTP_200_OK, \
        "Health endpoint should return 200 OK"
    
    # Parse JSON response
    data = response.json()
    
    # Assert response structure
    assert "status" in data, \
        "Health response should contain 'status' field"
    
    assert data["status"] == "healthy", \
        "Health status should be 'healthy'"


def test_health_endpoint_structure(client):
    """
    Test that health endpoint returns correct JSON structure.
    
    This ensures the response format is consistent and predictable.
    """
    response = client.get("/health")
    data = response.json()
    
    # Verify it's a dictionary (JSON object)
    assert isinstance(data, dict), \
        "Health response should be a JSON object"
    
    # Verify only expected fields are present
    assert set(data.keys()) == {"status"}, \
        "Health response should only contain 'status' field"

