"""
Main Publer API client.
"""

import os
from typing import Any, Dict, Optional

from dotenv import load_dotenv

from publer.models.posts import JobStatus
from publer.resources.accounts import AccountsResource, AsyncAccountsResource
from publer.resources.analytics import AnalyticsResource, AsyncAnalyticsResource
from publer.resources.media import AsyncMediaResource, MediaResource
from publer.resources.posts import AsyncPostsResource, PostsResource
from publer.resources.workspaces import AsyncWorkspacesResource, WorkspacesResource
from publer.session import AsyncPublerSession, PublerSession
from publer.utils.polling import poll_job_status, poll_job_status_async


class PublerClient:
    """
    Synchronous Publer API client.

    Example:
        >>> from publer import PublerClient
        >>> client = PublerClient(api_key="your_api_key")
        >>> user = client.me()
        >>> print(user["name"])
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        workspace_id: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: float = 30.0,
        load_env: bool = True,
    ) -> None:
        """
        Initialize the Publer API client.

        Args:
            api_key: Publer API key. If not provided, will try to load from
                     PUBLER_API_KEY environment variable.
            workspace_id: Optional workspace ID. If not provided, will try to load from
                         PUBLER_WORKSPACE_ID environment variable.
            base_url: API base URL. Defaults to https://app.publer.com/api/v1
            timeout: Request timeout in seconds
            load_env: Whether to load environment variables from .env file

        Raises:
            ValueError: If no API key is provided or found in environment

        Example:
            >>> # From parameters
            >>> client = PublerClient(api_key="your_key")
            >>>
            >>> # From environment variables
            >>> client = PublerClient()  # Loads from .env or environment
            >>>
            >>> # With workspace
            >>> client = PublerClient(api_key="your_key", workspace_id="workspace_123")
        """
        # Load .env file if requested
        if load_env:
            load_dotenv()

        # Get API key from parameter or environment
        self.api_key = api_key or os.getenv("PUBLER_API_KEY")
        if not self.api_key:
            raise ValueError(
                "API key is required. Provide it as a parameter or set PUBLER_API_KEY "
                "environment variable."
            )

        # Get optional configuration from environment
        self.workspace_id = workspace_id or os.getenv("PUBLER_WORKSPACE_ID")
        self.base_url = base_url or os.getenv(
            "PUBLER_BASE_URL", "https://app.publer.com/api/v1"
        )

        # Parse timeout from environment if not provided
        if timeout == 30.0:  # Default value
            env_timeout = os.getenv("PUBLER_TIMEOUT")
            if env_timeout:
                try:
                    timeout = float(env_timeout)
                except ValueError:
                    pass

        # Initialize session
        self._session = PublerSession(
            api_key=self.api_key,
            base_url=self.base_url,
            workspace_id=self.workspace_id,
            timeout=timeout,
        )

        # Initialize resources (lazy-loaded)
        self._workspaces: Optional[WorkspacesResource] = None
        self._accounts: Optional[AccountsResource] = None
        self._posts: Optional[PostsResource] = None
        self._media: Optional[MediaResource] = None
        self._analytics: Optional[AnalyticsResource] = None

    @property
    def workspaces(self) -> WorkspacesResource:
        """Access workspaces endpoints."""
        if self._workspaces is None:
            self._workspaces = WorkspacesResource(self._session)
        return self._workspaces

    @property
    def accounts(self) -> AccountsResource:
        """Access accounts endpoints."""
        if self._accounts is None:
            self._accounts = AccountsResource(self._session)
        return self._accounts

    @property
    def posts(self) -> PostsResource:
        """Access posts endpoints."""
        if self._posts is None:
            self._posts = PostsResource(self._session)
        return self._posts

    @property
    def media(self) -> MediaResource:
        """Access media endpoints."""
        if self._media is None:
            self._media = MediaResource(self._session)
        return self._media

    @property
    def analytics(self) -> AnalyticsResource:
        """Access analytics endpoints."""
        if self._analytics is None:
            self._analytics = AnalyticsResource(self._session)
        return self._analytics

    def set_workspace(self, workspace_id: str) -> None:
        """
        Set the active workspace for subsequent requests.

        Args:
            workspace_id: Workspace ID to use

        Example:
            >>> client.set_workspace("workspace_123")
        """
        self.workspace_id = workspace_id
        self._session.set_workspace(workspace_id)

    def job_status(self, job_id: str, poll: bool = False, timeout: float = 60.0) -> JobStatus:
        """
        Get the status of an async job.

        Args:
            job_id: Job ID to check
            poll: If True, poll until job completes or times out
            timeout: Maximum time to wait when polling (seconds)

        Returns:
            JobStatus object

        Raises:
            JobTimeoutError: If polling times out
            JobFailedError: If job fails
            PublerAPIError: If the request fails

        Example:
            >>> result = client.posts.create(text="Hello", accounts=["acc_1"])
            >>> status = client.job_status(result["job_id"], poll=True)
            >>> print(status.status)
            completed
        """
        if poll:
            return poll_job_status(self._session, job_id, timeout=timeout)
        else:
            response = self._session.request("GET", f"/job_status/{job_id}")
            return JobStatus(**response)

    def close(self) -> None:
        """
        Close the HTTP client and release resources.

        Example:
            >>> client = PublerClient(api_key="your_key")
            >>> # ... use client ...
            >>> client.close()
        """
        self._session.close()

    def __enter__(self) -> "PublerClient":
        """
        Context manager entry.

        Example:
            >>> with PublerClient(api_key="your_key") as client:
            ...     user = client.me()
        """
        return self

    def __exit__(self, *args: Any) -> None:
        """Context manager exit."""
        self.close()


class AsyncPublerClient:
    """
    Asynchronous Publer API client.

    Example:
        >>> import asyncio
        >>> from publer import AsyncPublerClient
        >>>
        >>> async def main():
        ...     async with AsyncPublerClient(api_key="your_key") as client:
        ...         user = await client.me()
        ...         print(user["name"])
        >>>
        >>> asyncio.run(main())
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        workspace_id: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: float = 30.0,
        load_env: bool = True,
    ) -> None:
        """
        Initialize the async Publer API client.

        Args:
            api_key: Publer API key. If not provided, will try to load from
                     PUBLER_API_KEY environment variable.
            workspace_id: Optional workspace ID. If not provided, will try to load from
                         PUBLER_WORKSPACE_ID environment variable.
            base_url: API base URL. Defaults to https://app.publer.com/api/v1
            timeout: Request timeout in seconds
            load_env: Whether to load environment variables from .env file

        Raises:
            ValueError: If no API key is provided or found in environment
        """
        # Load .env file if requested
        if load_env:
            load_dotenv()

        # Get API key from parameter or environment
        self.api_key = api_key or os.getenv("PUBLER_API_KEY")
        if not self.api_key:
            raise ValueError(
                "API key is required. Provide it as a parameter or set PUBLER_API_KEY "
                "environment variable."
            )

        # Get optional configuration from environment
        self.workspace_id = workspace_id or os.getenv("PUBLER_WORKSPACE_ID")
        self.base_url = base_url or os.getenv(
            "PUBLER_BASE_URL", "https://app.publer.com/api/v1"
        )

        # Parse timeout from environment if not provided
        if timeout == 30.0:  # Default value
            env_timeout = os.getenv("PUBLER_TIMEOUT")
            if env_timeout:
                try:
                    timeout = float(env_timeout)
                except ValueError:
                    pass

        # Initialize session
        self._session = AsyncPublerSession(
            api_key=self.api_key,
            base_url=self.base_url,
            workspace_id=self.workspace_id,
            timeout=timeout,
        )

        # Initialize resources (lazy-loaded)
        self._workspaces: Optional[AsyncWorkspacesResource] = None
        self._accounts: Optional[AsyncAccountsResource] = None
        self._posts: Optional[AsyncPostsResource] = None
        self._media: Optional[AsyncMediaResource] = None
        self._analytics: Optional[AsyncAnalyticsResource] = None

    @property
    def workspaces(self) -> AsyncWorkspacesResource:
        """Access workspaces endpoints."""
        if self._workspaces is None:
            self._workspaces = AsyncWorkspacesResource(self._session)
        return self._workspaces

    @property
    def accounts(self) -> AsyncAccountsResource:
        """Access accounts endpoints."""
        if self._accounts is None:
            self._accounts = AsyncAccountsResource(self._session)
        return self._accounts

    @property
    def posts(self) -> AsyncPostsResource:
        """Access posts endpoints."""
        if self._posts is None:
            self._posts = AsyncPostsResource(self._session)
        return self._posts

    @property
    def media(self) -> AsyncMediaResource:
        """Access media endpoints."""
        if self._media is None:
            self._media = AsyncMediaResource(self._session)
        return self._media

    @property
    def analytics(self) -> AsyncAnalyticsResource:
        """Access analytics endpoints."""
        if self._analytics is None:
            self._analytics = AsyncAnalyticsResource(self._session)
        return self._analytics

    def set_workspace(self, workspace_id: str) -> None:
        """
        Set the active workspace for subsequent requests.

        Args:
            workspace_id: Workspace ID to use
        """
        self.workspace_id = workspace_id
        self._session.set_workspace(workspace_id)

    async def job_status(
        self, job_id: str, poll: bool = False, timeout: float = 60.0
    ) -> JobStatus:
        """
        Get the status of an async job.

        Args:
            job_id: Job ID to check
            poll: If True, poll until job completes or times out
            timeout: Maximum time to wait when polling (seconds)

        Returns:
            JobStatus object

        Raises:
            JobTimeoutError: If polling times out
            JobFailedError: If job fails
            PublerAPIError: If the request fails

        Example:
            >>> result = await client.posts.create(text="Hello", accounts=["acc_1"])
            >>> status = await client.job_status(result["job_id"], poll=True)
            >>> print(status.status)
        """
        if poll:
            return await poll_job_status_async(self._session, job_id, timeout=timeout)
        else:
            response = await self._session.request("GET", f"/job_status/{job_id}")
            return JobStatus(**response)

    async def close(self) -> None:
        """Close the HTTP client and release resources."""
        await self._session.close()

    async def __aenter__(self) -> "AsyncPublerClient":
        """Async context manager entry."""
        return self

    async def __aexit__(self, *args: Any) -> None:
        """Async context manager exit."""
        await self.close()
