"""
Tests for exception classes.
"""

import pytest

from publer.exceptions import (
    AuthenticationError,
    NotFoundError,
    PublerAPIError,
    RateLimitError,
    ValidationError,
    get_exception_for_status,
)


def test_base_exception() -> None:
    """Test base PublerAPIError."""
    error = PublerAPIError(
        message="Test error",
        status_code=400,
        response={"data": "test"},
        errors=["Error 1", "Error 2"],
    )

    assert error.message == "Test error"
    assert error.status_code == 400
    assert error.response == {"data": "test"}
    assert error.errors == ["Error 1", "Error 2"]
    assert str(error) == "[400] Test error"


def test_rate_limit_error() -> None:
    """Test RateLimitError with retry_after."""
    error = RateLimitError(
        message="Rate limit exceeded",
        status_code=429,
        retry_after=60,
    )

    assert error.retry_after == 60
    assert "retry after 60s" in str(error)


def test_get_exception_for_status_400() -> None:
    """Test getting ValidationError for 400 status."""
    error = get_exception_for_status(
        status_code=400,
        message="Invalid data",
        errors=["Field is required"],
    )

    assert isinstance(error, ValidationError)
    assert error.status_code == 400
    assert error.message == "Invalid data"


def test_get_exception_for_status_401() -> None:
    """Test getting AuthenticationError for 401 status."""
    error = get_exception_for_status(
        status_code=401,
        message="Unauthorized",
    )

    assert isinstance(error, AuthenticationError)
    assert error.status_code == 401


def test_get_exception_for_status_404() -> None:
    """Test getting NotFoundError for 404 status."""
    error = get_exception_for_status(
        status_code=404,
        message="Not found",
    )

    assert isinstance(error, NotFoundError)
    assert error.status_code == 404


def test_get_exception_for_status_429() -> None:
    """Test getting RateLimitError for 429 status."""
    error = get_exception_for_status(
        status_code=429,
        message="Too many requests",
        response={"retry_after": 120},
    )

    assert isinstance(error, RateLimitError)
    assert error.status_code == 429
    assert error.retry_after == 120


def test_get_exception_for_status_unknown() -> None:
    """Test getting generic PublerAPIError for unknown status."""
    error = get_exception_for_status(
        status_code=418,  # I'm a teapot
        message="Unknown error",
    )

    assert isinstance(error, PublerAPIError)
    assert error.status_code == 418
