"""
Tests for Model Info Endpoint

Tests verify that the model information endpoint returns correct metadata.
"""

import pytest
from fastapi import status


def test_model_info_endpoint(client):
    """
    Test that the model info endpoint returns model metadata.
    
    What we're testing:
    - Endpoint exists and is accessible
    - Returns 200 status code
    - Returns all required fields (model_name, model_version, status, description)
    
    Why this matters:
    - Clients need to know which model version they're using
    - Useful for debugging and monitoring
    - Helps track model deployments
    """
    # Make GET request to /api/v1/model
    response = client.get("/api/v1/model")
    
    # Assert status code is 200 (OK)
    assert response.status_code == status.HTTP_200_OK, \
        "Model info endpoint should return 200 OK"
    
    # Parse JSON response
    data = response.json()
    
    # Assert all required fields are present
    required_fields = ["model_name", "model_version", "status", "description"]
    for field in required_fields:
        assert field in data, \
            f"Model info response should contain '{field}' field"
    
    # Assert field types
    assert isinstance(data["model_name"], str), \
        "model_name should be a string"
    assert isinstance(data["model_version"], str), \
        "model_version should be a string"
    assert isinstance(data["status"], str), \
        "status should be a string"
    assert isinstance(data["description"], str), \
        "description should be a string"


def test_model_info_values(client):
    """
    Test that model info returns expected values.
    
    This verifies the model service is correctly configured.
    """
    response = client.get("/api/v1/model")
    data = response.json()
    
    # Check that values are not empty
    assert data["model_name"] != "", \
        "model_name should not be empty"
    assert data["model_version"] != "", \
        "model_version should not be empty"
    assert data["status"] != "", \
        "status should not be empty"

