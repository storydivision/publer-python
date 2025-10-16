"""
Pytest configuration and shared fixtures.
"""

import pytest

from publer import AsyncPublerClient, PublerClient


@pytest.fixture
def mock_api_key() -> str:
    """Return a mock API key for testing."""
    return "test_api_key_12345"


@pytest.fixture
def mock_workspace_id() -> str:
    """Return a mock workspace ID for testing."""
    return "workspace_test_123"


@pytest.fixture
def client(mock_api_key: str) -> PublerClient:
    """
    Create a test client instance.

    Note: This client won't make real API calls in tests.
    Use respx or similar to mock HTTP requests.
    """
    return PublerClient(api_key=mock_api_key, load_env=False)


@pytest.fixture
async def async_client(mock_api_key: str) -> AsyncPublerClient:
    """
    Create a test async client instance.

    Note: This client won't make real API calls in tests.
    Use respx or similar to mock HTTP requests.
    """
    client = AsyncPublerClient(api_key=mock_api_key, load_env=False)
    yield client
    await client.close()
