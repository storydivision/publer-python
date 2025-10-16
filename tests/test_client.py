"""
Tests for the main client classes.
"""

import os

import pytest

from publer import AsyncPublerClient, PublerClient
from publer.exceptions import AuthenticationError


def test_client_initialization_with_api_key() -> None:
    """Test client initialization with explicit API key."""
    client = PublerClient(api_key="test_key", load_env=False)
    assert client.api_key == "test_key"
    assert client.base_url == "https://app.publer.com/api/v1"
    client.close()


def test_client_initialization_without_api_key() -> None:
    """Test that client raises error when no API key is provided."""
    with pytest.raises(ValueError, match="API key is required"):
        PublerClient(load_env=False)


def test_client_initialization_from_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test client initialization from environment variables."""
    monkeypatch.setenv("PUBLER_API_KEY", "env_test_key")
    monkeypatch.setenv("PUBLER_WORKSPACE_ID", "env_workspace_123")
    monkeypatch.setenv("PUBLER_TIMEOUT", "60")

    client = PublerClient(load_env=False)
    assert client.api_key == "env_test_key"
    assert client.workspace_id == "env_workspace_123"
    client.close()


def test_client_set_workspace() -> None:
    """Test setting workspace ID."""
    client = PublerClient(api_key="test_key", load_env=False)
    client.set_workspace("new_workspace_123")
    assert client.workspace_id == "new_workspace_123"
    client.close()


def test_client_context_manager() -> None:
    """Test client as context manager."""
    with PublerClient(api_key="test_key", load_env=False) as client:
        assert client.api_key == "test_key"
    # Client should be closed after context


@pytest.mark.asyncio
async def test_async_client_initialization() -> None:
    """Test async client initialization."""
    async with AsyncPublerClient(api_key="test_key", load_env=False) as client:
        assert client.api_key == "test_key"
        assert client.base_url == "https://app.publer.com/api/v1"


@pytest.mark.asyncio
async def test_async_client_without_api_key() -> None:
    """Test that async client raises error when no API key is provided."""
    with pytest.raises(ValueError, match="API key is required"):
        AsyncPublerClient(load_env=False)


def test_custom_base_url() -> None:
    """Test client with custom base URL."""
    custom_url = "https://custom.api.com/v1"
    client = PublerClient(api_key="test_key", base_url=custom_url, load_env=False)
    assert client.base_url == custom_url
    client.close()


def test_custom_timeout() -> None:
    """Test client with custom timeout."""
    client = PublerClient(api_key="test_key", timeout=60.0, load_env=False)
    assert client._session.timeout == 60.0
    client.close()
