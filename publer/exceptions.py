"""
Custom exceptions for the Publer API client.
"""

from typing import Any, Dict, List, Optional


class PublerAPIError(Exception):
    """Base exception for all Publer API errors."""

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        response: Optional[Dict[str, Any]] = None,
        errors: Optional[List[str]] = None,
    ) -> None:
        """
        Initialize a Publer API error.

        Args:
            message: Error message
            status_code: HTTP status code
            response: Full response data
            errors: List of error messages from API
        """
        self.message = message
        self.status_code = status_code
        self.response = response
        self.errors = errors or []
        super().__init__(self.message)

    def __str__(self) -> str:
        """Return string representation of the error."""
        if self.status_code:
            return f"[{self.status_code}] {self.message}"
        return self.message


class ValidationError(PublerAPIError):
    """400 Bad Request - Invalid request data."""

    pass


class AuthenticationError(PublerAPIError):
    """401 Unauthorized - Invalid or missing API key."""

    pass


class ForbiddenError(PublerAPIError):
    """403 Forbidden - Insufficient permissions."""

    pass


class NotFoundError(PublerAPIError):
    """404 Not Found - Resource does not exist."""

    pass


class RateLimitError(PublerAPIError):
    """429 Too Many Requests - Rate limit exceeded."""

    def __init__(
        self,
        message: str,
        retry_after: Optional[int] = None,
        **kwargs: Any,
    ) -> None:
        """
        Initialize a rate limit error.

        Args:
            message: Error message
            retry_after: Seconds to wait before retrying
            **kwargs: Additional arguments passed to PublerAPIError
        """
        super().__init__(message, **kwargs)
        self.retry_after = retry_after

    def __str__(self) -> str:
        """Return string representation with retry information."""
        base = super().__str__()
        if self.retry_after:
            return f"{base} (retry after {self.retry_after}s)"
        return base


class ServerError(PublerAPIError):
    """500+ Server Error - Internal server error."""

    pass


class JobTimeoutError(PublerAPIError):
    """Job polling timed out."""

    pass


class JobFailedError(PublerAPIError):
    """Async job failed."""

    pass


# Map HTTP status codes to exception classes
ERROR_MAP: Dict[int, type[PublerAPIError]] = {
    400: ValidationError,
    401: AuthenticationError,
    403: ForbiddenError,
    404: NotFoundError,
    429: RateLimitError,
    500: ServerError,
    502: ServerError,
    503: ServerError,
    504: ServerError,
}


def get_exception_for_status(
    status_code: int,
    message: str,
    response: Optional[Dict[str, Any]] = None,
    errors: Optional[List[str]] = None,
) -> PublerAPIError:
    """
    Get the appropriate exception class for an HTTP status code.

    Args:
        status_code: HTTP status code
        message: Error message
        response: Full response data
        errors: List of error messages

    Returns:
        Appropriate exception instance
    """
    exception_class = ERROR_MAP.get(status_code, PublerAPIError)

    # Special handling for rate limit errors
    if status_code == 429:
        retry_after = None
        if response:
            # Try to extract retry-after from response
            retry_after = response.get("retry_after")
        return RateLimitError(
            message=message,
            status_code=status_code,
            response=response,
            errors=errors,
            retry_after=retry_after,
        )

    return exception_class(
        message=message,
        status_code=status_code,
        response=response,
        errors=errors,
    )
