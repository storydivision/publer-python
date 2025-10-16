"""
Publer API Python Client

A modern, type-safe Python client library for the Publer API.
"""

from publer.client import AsyncPublerClient, PublerClient
from publer.exceptions import (
    AuthenticationError,
    ForbiddenError,
    JobFailedError,
    JobTimeoutError,
    NotFoundError,
    PublerAPIError,
    RateLimitError,
    ServerError,
    ValidationError,
)
from publer.models import (
    Account,
    JobStatus,
    Media,
    MediaUpload,
    Post,
    PostCreate,
    PostUpdate,
    Workspace,
)

__version__ = "0.2.0"
__all__ = [
    # Clients
    "PublerClient",
    "AsyncPublerClient",
    # Exceptions
    "PublerAPIError",
    "AuthenticationError",
    "ValidationError",
    "ForbiddenError",
    "NotFoundError",
    "RateLimitError",
    "ServerError",
    "JobTimeoutError",
    "JobFailedError",
    # Models
    "Workspace",
    "Account",
    "Post",
    "PostCreate",
    "PostUpdate",
    "JobStatus",
    "Media",
    "MediaUpload",
]
