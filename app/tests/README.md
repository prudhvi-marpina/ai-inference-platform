# Test Suite for AI Inference Platform

This directory contains automated tests for the AI Inference Platform.

## What Are Tests?

Tests are code that verifies your application works correctly. They:
- **Prevent bugs**: Catch errors before users do
- **Document behavior**: Show how the code should work
- **Enable refactoring**: Let you change code confidently
- **Improve quality**: Ensure features work as expected

## Test Structure

```
app/tests/
├── __init__.py          # Makes this a Python package
├── conftest.py          # Shared test fixtures (reusable test components)
├── test_health.py       # Tests for /health endpoint
├── test_model_info.py   # Tests for /api/v1/model endpoint
├── test_inference.py    # Tests for /api/v1/infer endpoint
└── test_rate_limit.py   # Tests for rate limiting
```

## Running Tests

### Run All Tests
```bash
pytest
```

### Run Specific Test File
```bash
pytest app/tests/test_health.py
```

### Run Specific Test Function
```bash
pytest app/tests/test_health.py::test_health_endpoint
```

### Run with Verbose Output
```bash
pytest -v
```

### Run with Coverage Report
```bash
pytest --cov=app --cov-report=html
```

## Test Categories

### Unit Tests
- Test individual functions/components in isolation
- Fast execution
- No external dependencies

### Integration Tests
- Test how components work together
- May use mock services (like mock Redis)
- Verify end-to-end behavior

## What Each Test File Tests

### `test_health.py`
- Health endpoint returns correct status
- Response format is correct

### `test_model_info.py`
- Model info endpoint returns metadata
- All required fields are present

### `test_inference.py`
- Inference endpoint accepts valid requests
- Input validation works (rejects invalid input)
- Caching behavior (cache hit/miss)
- Response format is correct

### `test_rate_limit.py`
- Rate limiting allows requests within limit
- Rate limiting blocks excessive requests
- Rate limiting can be disabled

## Test Fixtures (conftest.py)

Fixtures are reusable test components:

- **`client`**: FastAPI test client for making HTTP requests
- **`mock_redis`**: Mock Redis client for testing without real Redis
- **`mock_redis_connected`**: Mock Redis connected to cache service
- **`sample_inference_request`**: Sample request data
- **`sample_inference_response`**: Sample response data

## Writing New Tests

1. Create a new file: `test_feature_name.py`
2. Import pytest and your fixtures
3. Write test functions starting with `test_`
4. Use assertions to verify expected behavior

Example:
```python
def test_my_feature(client):
    response = client.get("/my-endpoint")
    assert response.status_code == 200
    assert "expected_field" in response.json()
```

## Best Practices

1. **Test one thing per test**: Each test should verify one behavior
2. **Use descriptive names**: Test names should explain what they test
3. **Keep tests independent**: Tests shouldn't depend on each other
4. **Use fixtures**: Reuse common test setup
5. **Mock external services**: Don't require real Redis/Database for unit tests

